import math
from decimal import Decimal
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from task.models import Task, TaskPrediction, TaskProgress


class DelayPredictionService:
    """
    Predicts probability of task delay using PERT-based estimation.
    """

    MODEL_NAME = "PERT_DELAY_MODEL"

    def __init__(self, project):
        self.project = project
        self.now = timezone.now()

    # ---------- Math helpers ----------

    def _normal_cdf(self, z):
        """
        Standard normal cumulative distribution function.
        """
        return Decimal(0.5 * (1 + math.erf(z / math.sqrt(2))))

    def _latest_progress(self, task):
        return (
            TaskProgress.objects
            .filter(task=task)
            .order_by("-snapshot_time")
            .first()
        )

    # ---------- Core logic ----------

    def _predict_task_delay(self, task):
        # Ensure PERT inputs exist
        if not all([
            task.optimistic_hours,
            task.most_likely_hours,
            task.pessimistic_hours,
            task.planned_finish,
        ]):
            return None

        # Expected duration & variance
        o = Decimal(task.optimistic_hours)
        m = Decimal(task.most_likely_hours)
        p = Decimal(task.pessimistic_hours)

        expected_duration = (o + 4 * m + p) / Decimal(6)
        variance = ((p - o) / Decimal(6)) ** 2
        std_dev = variance.sqrt() if variance > 0 else Decimal("0.0")

        # Remaining time
        remaining_seconds = (task.planned_finish - self.now).total_seconds()
        remaining_hours = Decimal(remaining_seconds / 3600)

        if remaining_hours <= 0:
            return Decimal("1.0")  # already late

        # Remaining expected work
        progress = self._latest_progress(task)
        completed_ratio = (
            Decimal(progress.percent_complete) / Decimal("100.0")
            if progress else Decimal("0.0")
        )
        remaining_expected = expected_duration * (Decimal("1.0") - completed_ratio)

        if std_dev == 0:
            return Decimal("1.0") if remaining_expected > remaining_hours else Decimal("0.0")

        # Z-score
        z = (remaining_hours - remaining_expected) / std_dev
        delay_probability = Decimal("1.0") - self._normal_cdf(float(z))

        return max(Decimal("0.0"), min(Decimal("1.0"), delay_probability))

    # ---------- Execution ----------

    @transaction.atomic
    def run(self):
        tasks = Task.objects.filter(project=self.project)

        predictions = []

        for task in tasks:
            prob = self._predict_task_delay(task)
            if prob is None:
                continue

            prediction = TaskPrediction.objects.create(
                task=task,
                generated_at=self.now,
                model_name=self.MODEL_NAME,
                probability_of_delay=prob.quantize(Decimal("0.0001")),
                details={
                    "method": "PERT",
                    "optimistic": float(task.optimistic_hours),
                    "most_likely": float(task.most_likely_hours),
                    "pessimistic": float(task.pessimistic_hours),
                    "planned_finish": task.planned_finish.isoformat(),
                },
            )
            predictions.append(prediction)

        return predictions
