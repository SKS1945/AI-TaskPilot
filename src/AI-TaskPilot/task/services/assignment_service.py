from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from task.models import (
    Task,
    TaskAssignment,
    TaskAssignmentHistory,
)
from resource.models import Resource, ResourceAvailability
from skill.models import ResourceSkill


class SmartAssignmentService:
    """
    Assigns tasks to the most suitable resource based on:
    - skill match
    - current workload
    - availability across projects
    """

    SKILL_WEIGHT = Decimal("5.0")
    WORKLOAD_WEIGHT = Decimal("1.0")
    AVAILABILITY_WEIGHT = Decimal("1.5")

    def __init__(self, project, *, dry_run=False):
        self.project = project
        self.dry_run = dry_run
        self.now = timezone.now()

    # ---------- Data fetch helpers ----------

    def _get_unlocked_tasks(self):
        return Task.objects.filter(
            project=self.project,
            status__in=["todo", "in_progress"],
        ).exclude(assignments__locked=True)

    def _latest_availability(self):
        """
        Returns {resource_id: ResourceAvailability}
        """
        latest = {}
        qs = (
            ResourceAvailability.objects
            .select_related("resource")
            .order_by("resource_id", "-snapshot_time")
        )
        for ra in qs:
            if ra.resource_id not in latest:
                latest[ra.resource_id] = ra
        return latest

    def _resource_skills(self):
        """
        Returns {resource_id: {skill_name: proficiency}}
        """
        skills = defaultdict(dict)
        for rs in ResourceSkill.objects.select_related("resource", "skill"):
            skills[rs.resource_id][rs.skill.name] = rs.proficiency_level or 1
        return skills

    def _current_workload(self):
        """
        Returns {resource_id: total_allocated_effort}
        """
        workload = defaultdict(Decimal)
        for a in TaskAssignment.objects.filter(
            task__project=self.project
        ):
            if a.allocated_effort:
                workload[a.resource_id] += a.allocated_effort
        return workload

    # ---------- Scoring ----------

    def _skill_score(self, task, resource_skills):
        """
        Basic heuristic:
        - If task.metadata contains required_skills, match against them
        """
        required = task.metadata.get("required_skills", [])
        if not required:
            return Decimal("1.0")  # neutral baseline

        score = Decimal("0.0")
        for s in required:
            if s in resource_skills:
                score += Decimal(resource_skills[s])
        return score

    def _compute_score(self, task, resource, context):
        skill_score = self._skill_score(
            task, context["skills"].get(resource.id, {})
        )

        workload_penalty = context["workload"].get(resource.id, Decimal("0.0"))
        availability = context["availability"].get(resource.id)

        availability_penalty = Decimal("0.0")
        if availability:
            if availability.available_hours <= 0:
                availability_penalty = Decimal("100.0")
            else:
                availability_penalty = (
                    availability.committed_hours / availability.available_hours
                )

        return (
            self.SKILL_WEIGHT * skill_score
            - self.WORKLOAD_WEIGHT * workload_penalty
            - self.AVAILABILITY_WEIGHT * availability_penalty
        )

    # ---------- Core execution ----------

    @transaction.atomic
    def run(self):
        tasks = self._get_unlocked_tasks()
        if not tasks.exists():
            return []

        context = {
            "availability": self._latest_availability(),
            "skills": self._resource_skills(),
            "workload": self._current_workload(),
        }

        resources = Resource.objects.filter(is_active=True)

        assignments_made = []

        for task in tasks:
            best_resource = None
            best_score = None

            for resource in resources:
                score = self._compute_score(task, resource, context)

                if best_score is None or score > best_score:
                    best_score = score
                    best_resource = resource

            if not best_resource:
                continue

            if self.dry_run:
                assignments_made.append((task, best_resource, best_score))
                continue

            assignment = TaskAssignment.objects.create(
                task=task,
                resource=best_resource,
                assigned_at=self.now,
                is_primary=True,
            )

            TaskAssignmentHistory.objects.create(
                task=task,
                resource=best_resource,
                timestamp=self.now,
                action="auto_assign",
                actor="system",
                reason="Smart assignment based on skill/workload/availability",
                metadata={"score": str(best_score)},
            )

            assignments_made.append(assignment)

        return assignments_made
