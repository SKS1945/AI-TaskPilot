from django.db import models
from resource.models import Resource

# Create your models here.



class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class ResourceSkill(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('resource', 'skill')
