from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from project.models import Project
from task.models import Task
from task.services.assignment_service import SmartAssignmentService
from task.services.progress_monitoring_service import ProgressMonitoringService
from task.services.delay_prediction_service import DelayPredictionService


class TaskListAPIView(APIView):
    """
    Returns tasks for the 'Tasks' list or Gantt Chart.
    """

    def get(self, request, project_id):
        tasks = Task.objects.filter(project_id=project_id).values(
            "id", "title", "status", "priority",  # 'weight' mapped to priority in frontend
            "planned_start", "planned_finish",
            "is_on_critical_path", "assigned_to__display_name"  # Assuming logical join
        )
        return Response(list(tasks))

    def post(self, request, project_id):
        """Create a new task directly from the UI"""
        project = get_object_or_404(Project, id=project_id)
        data = request.data
        task = Task.objects.create(
            project=project,
            title=data.get('title'),
            description=data.get('description', ''),
            planned_start=data.get('planned_start'),
            planned_finish=data.get('planned_finish'),
            weight=data.get('weight', 1)
        )
        return Response({"id": task.id, "message": "Task created"}, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):
    """
    Handles updating a single task (e.g. status change, dragging on timeline).
    """

    def patch(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        data = request.data

        if 'status' in data:
            task.status = data['status']
        if 'planned_start' in data:
            task.planned_start = data['planned_start']
        if 'planned_finish' in data:
            task.planned_finish = data['planned_finish']

        task.save()
        return Response({"id": task.id, "message": "Task updated"}, status=status.HTTP_200_OK)


class AutoAssignTaskAPIView(APIView):
    """
    Runs smart assignment for a project.
    """

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        assignments = SmartAssignmentService(project).run()
        return Response(
            {"assigned_tasks_count": len(assignments)},
            status=status.HTTP_200_OK
        )


class MonitorProgressAPIView(APIView):
    """
    Computes task + project health.
    """

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
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
        project = get_object_or_404(Project, id=project_id)
        predictions = DelayPredictionService(project).run()
        return Response(
            {"predictions_created": len(predictions)},
            status=status.HTTP_200_OK
        )