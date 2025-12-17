from datetime import timedelta
from django.utils.timezone import now

from project.services.risk import compute_project_delay_risk
from notification.models import Notification, NotificationRule
from task.models import Task


PROJECT_RISK_THRESHOLD = 0.30
NEAR_DEADLINE_HOURS = 48


def trigger_project_risk_notifications(project):
    risk_data = compute_project_delay_risk(project)

    if risk_data["project_delay_probability"] < PROJECT_RISK_THRESHOLD:
        return []

    rule, _ = NotificationRule.objects.get_or_create(
        target_type="project",
        project=project,
        trigger_type="project_risk_high",
        defaults={"channels": ["email"]}
    )

    notification = Notification.objects.create(
        rule=rule,
        target_type="project",
        content=(
            f"Project '{project.name}' has a high delay risk "
            f"({risk_data['risk_score']}%)."
        ),
        status="generated"
    )

    return [notification]


def trigger_task_deadline_notifications(task):
    notifications = []
    now_ts = now()

    if not task.planned_finish:
        return notifications

    # Near deadline
    if now_ts + timedelta(hours=NEAR_DEADLINE_HOURS) >= task.planned_finish:
        rule, _ = NotificationRule.objects.get_or_create(
            target_type="task",
            task=task,
            trigger_type="task_near_deadline",
            defaults={"channels": ["email"]}
        )

        notifications.append(
            Notification.objects.create(
                rule=rule,
                target_type="task",
                content=f"Task '{task.title}' is nearing its deadline.",
                status="generated"
            )
        )

    # Overdue
    if now_ts > task.planned_finish:
        rule, _ = NotificationRule.objects.get_or_create(
            target_type="task",
            task=task,
            trigger_type="task_overdue",
            defaults={"channels": ["email"]}
        )

        notifications.append(
            Notification.objects.create(
                rule=rule,
                target_type="task",
                content=f"Task '{task.title}' is overdue.",
                status="generated"
            )
        )

    return notifications
