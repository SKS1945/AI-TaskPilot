from django.db import models
from django.conf import settings

# Create your models here.



class Resource(models.Model):
    display_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    capacity_hours_per_week = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    team = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.display_name


class ResourceAvailability(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='availability')
    snapshot_time = models.DateTimeField(auto_now_add=True)
    committed_hours = models.DecimalField(max_digits=6, decimal_places=2)
    available_hours = models.DecimalField(max_digits=6, decimal_places=2)
    calendar_metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['resource', 'snapshot_time']),
        ]
