
from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Project(models.Model):
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=32, db_index=True)  # planning, active, paused, completed, archived
    planned_start = models.DateField(null=True, blank=True)
    planned_finish = models.DateField(null=True, blank=True)
    health_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       help_text='Cached 0-100 health metric')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['owner']),
        ]

    def __str__(self):
        return f"{self.key} - {self.name}"


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    is_mandatory = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.project.key}: {self.name}"


class TimelineSnapshot(models.Model):
    """
    Immutable snapshot of computed schedule: serialized AON + Gantt + summary.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timeline_snapshots')
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    network_json = models.JSONField()
    gantt_json = models.JSONField()
    summary = models.JSONField()  # e.g., {'critical_path': [...], 'expected_finish': 'YYYY-MM-DD'}

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
        ]

    def __str__(self):
        return f"TimelineSnapshot {self.project.key} @ {self.created_at.isoformat()}"


class ProjectReport(models.Model):
    """
    Project-level report (weekly/monthly/project).
    """
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name='reports')
    report_type = models.CharField(max_length=32)  # 'weekly', 'monthly', 'project'
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True)
    payload = models.JSONField()  # structured report content (KPIs, drilldowns)
    export_ref = models.CharField(max_length=512, blank=True, help_text='Optional file reference/path')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['report_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        proj = self.project.key if self.project else "Portfolio"
        return f"{proj} - {self.report_type} ({self.period_start}..{self.period_end})"
