from django.contrib import admin

# Register your models here.
from .models import (
    Task, TaskDependency, TaskProgress,
    TaskAssignment, TaskAssignmentHistory,
    TaskPrediction, TaskReport
)

admin.site.register(Task)
admin.site.register(TaskDependency)
admin.site.register(TaskProgress)
admin.site.register(TaskAssignment)
admin.site.register(TaskAssignmentHistory)
admin.site.register(TaskPrediction)
admin.site.register(TaskReport)
