from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from notification.models import NotificationRule, Notification
from task.models import Task, TaskProgress, TaskPrediction
from project.models import Project


class NotificationEvaluationService:
    """
    Evaluates NotificationRules and generates Notification records.
    """

    def __init__(self, now=None):
        self.now = now or timezone.now()

    # ---------- Helpers ----------

    def _latest_progress(self, task):
        return (
            TaskProgress.objects
            .filter(task=task)
            .order_by("-snapshot_time")
            .first()
        )

    def _latest_prediction(self, task):
        return (
            TaskPrediction.objects
            .filter(task=task)
            .order_by("-generated_at")
            .first()
        )

    def _create_notification(self, rule, target_type, target, content):
        Notification.objects.create(
            rule=rule,
            target_type=target_type,
            target_project=target if target_type == "project" else None,
            target_task=target if target_type == "task" else None,
            generated_at=self.now,
            channel="system",  # delivery handled later
            content=content,
            status="pending",
        )

    # ---------- Trigger evaluators ----------

    def _check_near_deadline(self, rule, task):
        if not task.planned_finish:
            return False

        threshold_hours = Decimal(rule.threshold or 0)
        delta = task.planned_finish - self.now

        return Decimal(delta.total_seconds() / 3600) <= threshold_hours

    def _check_predicted_delay(self, rule, task):
        prediction = self._latest_prediction(task)
        if not prediction:
            return False

        threshold = Decimal(rule.threshold or 0)
        return prediction.probability_of_delay >= threshold

    def _check_stale_progress(self, rule, task):
        progress = self._latest_progress(task)
        if not progress:
            return True  # never updated → stale

        threshold_days = int(rule.threshold or 0)
        return (self.now - progress.snapshot_time) >= timedelta(days=threshold_days)

    # ---------- Core Execution ----------

    @transaction.atomic
    def run(self):
        rules = NotificationRule.objects.all()

        generated = []

        for rule in rules:
            if rule.target_type == "project":
                projects = (
                    Project.objects.filter(id=rule.target_project_id)
                    if rule.target_project_id
                    else Project.objects.all()
                )

                for project in projects:
                    content = f"Notification for project {project.name} ({rule.trigger_type})"
                    self._create_notification(rule, "project", project, content)
                    generated.append((rule, project))

            elif rule.target_type == "task":
                tasks = (
                    Task.objects.filter(id=rule.target_task_id)
                    if rule.target_task_id
                    else Task.objects.all()
                )

                for task in tasks:
                    triggered = False

                    if rule.trigger_type == "near_deadline":
                        triggered = self._check_near_deadline(rule, task)

                    elif rule.trigger_type == "predicted_delay":
                        triggered = self._check_predicted_delay(rule, task)

                    elif rule.trigger_type == "stale_progress":
                        triggered = self._check_stale_progress(rule, task)

                    if triggered:
                        content = (
                            f"Task '{task.title}' triggered '{rule.trigger_type}' notification"
                        )
                        self._create_notification(rule, "task", task, content)
                        generated.append((rule, task))

        return generated
