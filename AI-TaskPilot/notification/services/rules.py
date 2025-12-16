from notification.models import NotificationRule


def get_applicable_rules(target_type, target_id):
    return NotificationRule.objects.filter(
        target_type=target_type
    ).filter(
        project_id=target_id if target_type == 'project' else None,
        task_id=target_id if target_type == 'task' else None
    )
