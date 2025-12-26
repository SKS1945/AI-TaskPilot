from datetime import timedelta
from django.utils.timezone import now


def is_near_deadline(task, threshold_hours=48):
    if not task.planned_finish:
        return False
    return task.planned_finish - now() <= timedelta(hours=threshold_hours)
