from notification.models import Notification


def dispatch_notification(rule, target, content, channel="email"):
    return Notification.objects.create(
        rule=rule,
        target_type=rule.target_type,
        channel=channel,
        content=content,
        status="sent"
    )
