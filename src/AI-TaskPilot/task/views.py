from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from task.models import Task
from task.services.assignment_service import SmartAssignmentService
from task.services.progress_monitoring_service import ProgressMonitoringService
from task.services.delay_prediction_service import DelayPredictionService


class TaskListAPIView(APIView):
    def get(self, request, project_id):
        tasks = Task.objects.filter(project_id=project_id).values(
            "id", "title", "status", "planned_start", "planned_finish",
            "is_on_critical_path"
        )
        return Response(list(tasks))


class AutoAssignTaskAPIView(APIView):
    """
    Runs smart assignment for a project.
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        assignments = SmartAssignmentService(project).run()

        return Response(
            {"assigned_tasks": len(assignments)},
            status=status.HTTP_200_OK
        )


class MonitorProgressAPIView(APIView):
    """
    Computes task + project health.
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        health = ProgressMonitoringService(project).run()

        return Response(
            {"project_health": float(health)},
            status=status.HTTP_200_OK
        )


class PredictDelayAPIView(APIView):
    """
    Runs PERT-based delay prediction.
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        predictions = DelayPredictionService(project).run()

        return Response(
            {"predictions_created": len(predictions)},
            status=status.HTTP_200_OK
        )
