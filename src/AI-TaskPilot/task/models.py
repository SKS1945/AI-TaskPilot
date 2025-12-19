
from django.db import models
from django.utils import timezone
from project.models import Project
from resource.models import Resource

# Create your models here.



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('review', 'In Review'),
        ('done', 'Done'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='todo', db_index=True)
    weight = models.PositiveSmallIntegerField(default=1, help_text='Business importance weight')
    planned_start = models.DateTimeField(null=True, blank=True)
    planned_finish = models.DateTimeField(null=True, blank=True)

    # PERT estimates (input)
    optimistic_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    most_likely_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pessimistic_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Derived (written by scheduling service)
    expected_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    variance = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    is_on_critical_path = models.BooleanField(default=False, db_index=True)
    total_float_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)  # AI suggestions, tags, etc.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['is_on_critical_path', 'status']),
            models.Index(fields=['project', 'updated_at']),
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.project.key} :: {self.title}"


class TaskDependency(models.Model):
    DEP_TYPE_CHOICES = [
        ('task_task', 'Task->Task'),
        ('resource_task', 'Resource->Task'),
    ]

    dependent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    dependency_type = models.CharField(max_length=24, choices=DEP_TYPE_CHOICES)
    predecessor_task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL, related_name='dependents')
    predecessor_resource = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.SET_NULL)
    predecessor_team = models.CharField(max_length=128, blank=True)
    lag_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['dependent_task']),
            models.Index(fields=['dependency_type']),
        ]

    def __str__(self):
        return f"Dependency for {self.dependent_task_id} ({self.dependency_type})"


class TaskProgress(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress_snapshots')
    snapshot_time = models.DateTimeField(default=timezone.now, db_index=True)
    percent_complete = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 0.00 - 100.00
    effort_consumed = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # hours
    status_note = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-snapshot_time']
        indexes = [
            models.Index(fields=['task', 'snapshot_time']),
        ]

    def __str__(self):
        return f"{self.task} @ {self.snapshot_time.isoformat()} ({self.percent_complete}%)"


class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    allocated_effort = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # hours
    is_primary = models.BooleanField(default=True)
    locked = models.BooleanField(default=False, help_text='When true, do not auto-reassign')

    class Meta:
        indexes = [
            models.Index(fields=['resource', 'start_date']),
            models.Index(fields=['task']),
        ]

    def __str__(self):
        return f"{self.resource} -> {self.task}"


class TaskAssignmentHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    action = models.CharField(max_length=32)  # assign, reassign, unassign, auto_suggested, etc.
    actor = models.CharField(max_length=128, blank=True)  # username or 'system'
    reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['task', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action} {self.resource} on {self.task} @ {self.timestamp.isoformat()}"


class TaskPrediction(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='predictions')
    generated_at = models.DateTimeField(default=timezone.now, db_index=True)
    model_name = models.CharField(max_length=128)
    probability_of_delay = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['task', 'generated_at']),
        ]

    def __str__(self):
        return f"Prediction {self.task} @ {self.generated_at.isoformat()}"


class TaskReport(models.Model):
    """
    Task-level reports: status summary, delay report, etc.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=32)  # 'status', 'delay', 'performance'
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    summary = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task', 'report_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"TaskReport {self.task} - {self.report_type}"
