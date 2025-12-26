from django.db import models
from project.models import Project
from resource.models import Resource

# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    weight = models.PositiveIntegerField(default=1)

    planned_start = models.DateTimeField(null=True, blank=True)
    planned_finish = models.DateTimeField(null=True, blank=True)

    # PERT fields
    optimistic_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    most_likely_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    pessimistic_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    expected_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    variance = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    is_on_critical_path = models.BooleanField(default=False)
    total_float_hours = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['is_on_critical_path']),
            models.Index(fields=['planned_finish']),
        ]


class TaskDependency(models.Model):
    DEPENDENCY_TYPE_CHOICES = [
        ('task', 'Task → Task'),
        ('resource', 'Resource → Task'),
    ]

    dependent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    dependency_type = models.CharField(max_length=20, choices=DEPENDENCY_TYPE_CHOICES)

    predecessor_task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dependent_links'
    )
    predecessor_resource = models.ForeignKey(
        Resource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    predecessor_team = models.CharField(max_length=100, blank=True)
    lag_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class TaskProgress(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress_entries')
    snapshot_time = models.DateTimeField(auto_now_add=True)
    percent_complete = models.DecimalField(max_digits=5, decimal_places=2)
    effort_consumed = models.DecimalField(max_digits=8, decimal_places=2)
    status_note = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='assignments')

    assigned_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    allocated_effort = models.DecimalField(max_digits=8, decimal_places=2)
    is_primary = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)


class TaskAssignmentHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    actor = models.CharField(max_length=100)
    reason = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class TaskPrediction(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='predictions')
    generated_at = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=100)
    probability_of_delay = models.DecimalField(max_digits=6, decimal_places=4)
    details = models.JSONField()


class TaskReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50)
    summary = models.TextField()
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
