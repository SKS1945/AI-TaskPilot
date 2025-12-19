
from django.db import models
from django.utils import timezone
from project.models import Project
from task.models import Task

# Create your models here.



class EscalationPolicy(models.Model):
    name = models.CharField(max_length=128)
    steps = models.JSONField(help_text='List of escalation steps with timing and recipients')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class NotificationRule(models.Model):
    """
    Defines when to trigger notifications.
    target_type: 'project' or 'task'
    trigger_type: 'near_deadline', 'predicted_delay', 'stale_progress', etc.
    channels: JSON list, e.g. ['email', 'slack']
    """
    TARGET_CHOICES = [('project', 'Project'), ('task', 'Task')]
    TRIGGER_CHOICES = [
        ('near_deadline', 'Near Deadline'),
        ('predicted_delay', 'Predicted Delay'),
        ('stale_progress', 'Stale Progress'),
    ]

    target_type = models.CharField(max_length=16, choices=TARGET_CHOICES)
    target_project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    target_task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    trigger_type = models.CharField(max_length=64, choices=TRIGGER_CHOICES)
    threshold = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True,
                                    help_text='Meaning depends on trigger (hours or probability)')
    channels = models.JSONField(default=list)  # ['email', 'slack']
    escalation_policy = models.ForeignKey(EscalationPolicy, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['target_type']),
            models.Index(fields=['trigger_type']),
        ]

    def __str__(self):
        tgt = self.target_project or self.target_task
        return f"Rule {self.trigger_type} -> {tgt}"


class Notification(models.Model):
    rule = models.ForeignKey(NotificationRule, on_delete=models.CASCADE, related_name='notifications')
    target_type = models.CharField(max_length=16)  # 'project' or 'task'
    target_project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    target_task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(default=timezone.now, db_index=True)
    channel = models.CharField(max_length=64)  # 'email', 'slack', etc.
    content = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, default='pending')  # pending, sent, failed
    response = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['rule']),
            models.Index(fields=['generated_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Notification {self.id} ({self.channel})"
