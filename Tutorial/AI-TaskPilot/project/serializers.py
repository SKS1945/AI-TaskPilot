from rest_framework import serializers
from project.models import TimelineSnapshot


class TimelineSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineSnapshot
        fields = [
            'id',
            'project',
            'created_at',
            'gantt_json',
            'summary'
        ]
