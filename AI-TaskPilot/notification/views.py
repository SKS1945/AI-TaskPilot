from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from notification.services.evaluator import evaluate_notifications_for_project
from notification.serializers import NotificationSerializer


class EvaluateNotificationsAPIView(APIView):
    """
    POST /api/projects/{project_id}/notifications/evaluate/
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        notifications = evaluate_notifications_for_project(project)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
