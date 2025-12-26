from django.db import models
from project.models import Project
from task.models import Task

# Create your models here.



class NotificationRule(models.Model):
    TARGET_TYPE_CHOICES = [
        ('project', 'Project'),
        ('task', 'Task'),
    ]

    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    trigger_type = models.CharField(max_length=50)
    threshold = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    channels = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    rule = models.ForeignKey(NotificationRule, on_delete=models.CASCADE, related_name='notifications')
    target_type = models.CharField(max_length=20)
    generated_at = models.DateTimeField(auto_now_add=True)

    channel = models.CharField(max_length=50)
    content = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)
    response = models.JSONField(default=dict, blank=True)
