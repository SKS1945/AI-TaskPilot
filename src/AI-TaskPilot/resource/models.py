from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.



class Resource(models.Model):
    """
    Represents a person / resource.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    display_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True, db_index=True)
    capacity_hours_per_week = models.DecimalField(max_digits=6, decimal_places=2, default=40.00)
    is_active = models.BooleanField(default=True)
    team = models.CharField(max_length=128, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.display_name


class ResourceAvailability(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='availability_snapshots')
    snapshot_time = models.DateTimeField(default=timezone.now, db_index=True)
    committed_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # across projects
    available_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    calendar_metadata = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-snapshot_time']
        indexes = [
            models.Index(fields=['resource', 'snapshot_time']),
        ]

    def __str__(self):
        return f"{self.resource} @ {self.snapshot_time.isoformat()}"

