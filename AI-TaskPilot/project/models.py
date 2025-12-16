from django.db import models
from django.conf import settings

# Create your models here.

class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    planned_start = models.DateField(null=True, blank=True)
    planned_finish = models.DateField(null=True, blank=True)
    health_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=255)
    due_date = models.DateField()
    is_mandatory = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.project.key} - {self.name}"


class TimelineSnapshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timeline_snapshots')
    created_at = models.DateTimeField(auto_now_add=True)

    network_json = models.JSONField()
    gantt_json = models.JSONField()
    summary = models.JSONField()

    def __str__(self):
        return f"TimelineSnapshot({self.project.key}, {self.created_at})"


class ProjectReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('project', 'Project'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports'
    )
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)

    summary = models.TextField()
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
