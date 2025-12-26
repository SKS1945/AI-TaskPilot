from rest_framework import serializers
from task.models import TaskAssignment
from resource.models import Resource


class ResourceLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'display_name', 'team']


class TaskAssignmentSerializer(serializers.ModelSerializer):
    resource = ResourceLiteSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = [
            'id',
            'task',
            'resource',
            'allocated_effort',
            'is_primary',
            'locked',
            'assigned_at'
        ]
        read_only_fields = ['assigned_at']

from task.models import TaskPrediction


class TaskPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPrediction
        fields = [
            'id',
            'task',
            'model_name',
            'probability_of_delay',
            'details',
            'generated_at'
        ]
