from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from task.models import Task, TaskProgress
from project.models import Project


class ProgressMonitoringService:
    """
    Computes task-level and project-level health
    based on progress vs schedule.
    """

    STALLED_DAYS_THRESHOLD = 3

    def __init__(self, project: Project):
        self.project = project
        self.now = timezone.now()

    # ---------- Helpers ----------

    def _latest_progress(self, task):
        return (
            TaskProgress.objects
            .filter(task=task)
            .order_by("-snapshot_time")
            .first()
        )

    def _expected_progress_ratio(self, task):
        if not task.planned_start or not task.planned_finish:
            return None

        total_seconds = (task.planned_finish - task.planned_start).total_seconds()
        elapsed_seconds = (self.now - task.planned_start).total_seconds()

        if total_seconds <= 0:
            return None

        return max(Decimal("0.0"), min(Decimal("1.0"), Decimal(elapsed_seconds / total_seconds)))

    def _task_health(self, task, progress):
        if not progress:
            return Decimal("0.0")

        expected_ratio = self._expected_progress_ratio(task)
        actual_ratio = Decimal(progress.percent_complete) / Decimal("100.0")

        if expected_ratio is None or expected_ratio == 0:
            return actual_ratio * Decimal("100.0")

        schedule_ratio = actual_ratio / expected_ratio

        if schedule_ratio >= 1:
            return Decimal("100.0")

        return max(Decimal("0.0"), schedule_ratio * Decimal("100.0"))

    def _is_stalled(self, progress):
        if not progress:
            return True

        delta_days = (self.now - progress.snapshot_time).days
        return delta_days >= self.STALLED_DAYS_THRESHOLD

    # ---------- Core Execution ----------

    @transaction.atomic
    def run(self):
        tasks = Task.objects.filter(project=self.project)

        if not tasks.exists():
            self.project.health_score = Decimal("0.0")
            self.project.save(update_fields=["health_score"])
            return self.project.health_score

        weighted_health_sum = Decimal("0.0")
        total_weight = Decimal("0.0")

        for task in tasks:
            progress = self._latest_progress(task)
            health = self._task_health(task, progress)

            # Store per-task derived signals in metadata
            task.metadata["health"] = float(health)
            task.metadata["stalled"] = self._is_stalled(progress)
            task.save(update_fields=["metadata"])

            weighted_health_sum += health * Decimal(task.weight)
            total_weight += Decimal(task.weight)

        project_health = (
            weighted_health_sum / total_weight
            if total_weight > 0
            else Decimal("0.0")
        )

        self.project.health_score = project_health.quantize(Decimal("0.01"))
        self.project.save(update_fields=["health_score"])

        return self.project.health_score
