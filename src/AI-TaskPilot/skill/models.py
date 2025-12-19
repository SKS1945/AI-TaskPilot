
from django.db import models
from resource.models import Resource

# Create your models here.



class Skill(models.Model):
    name = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=128, blank=True, db_index=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name


class ResourceSkill(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='resource_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='resource_skills')
    proficiency_level = models.PositiveSmallIntegerField(null=True, blank=True,
                                                        help_text='Optional 1-5 proficiency level')

    class Meta:
        unique_together = ('resource', 'skill')
        indexes = [
            models.Index(fields=['resource', 'skill']),
        ]

    def __str__(self):
        return f"{self.resource} - {self.skill} ({self.proficiency_level})"

