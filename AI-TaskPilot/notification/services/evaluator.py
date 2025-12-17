from notification.services.triggers import (
    trigger_project_risk_notifications,
    trigger_task_deadline_notifications
)
from task.models import Task


def evaluate_notifications_for_project(project):
    notifications = []

    notifications.extend(
        trigger_project_risk_notifications(project)
    )

    tasks = Task.objects.filter(project=project)
    for task in tasks:
        notifications.extend(
            trigger_task_deadline_notifications(task)
        )

    return notifications
