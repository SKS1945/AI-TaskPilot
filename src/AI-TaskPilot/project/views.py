from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.utils import timezone

from project.models import Project, Milestone
from task.models import Task, TaskPrediction
from project.services.timeline_service import TimelinePlanningService


class ProjectListAPIView(APIView):
    """
    Used for the 'Projects' page list.
    """

    def get(self, request):
        projects = Project.objects.all().values(
            "id", "key", "name", "status", "health_score", "owner__username", "updated_at"
        )
        return Response(list(projects))


class ProjectContextAPIView(APIView):
    """
    Lightweight endpoint for the Top Navigation Bar Project Switcher.
    """

    def get(self, request):
        projects = Project.objects.filter(status__in=['planning', 'active']).values("id", "name")
        return Response(list(projects))


class ProjectDashboardAPIView(APIView):
    """
    Powers the Main Dashboard Page.
    Aggregates Health, Active Risks (Predicted Delays), and Upcoming Deadlines.
    """

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # 1. High-Level Snapshot
        snapshot = {
            "name": project.name,
            "status": project.status,
            "health_score": project.health_score,
            "planned_finish": project.planned_finish,
        }

        # 2. Active Risks (High Probability Delays)
        # Fetch tasks with > 50% delay probability
        high_risk_predictions = TaskPrediction.objects.filter(
            task__project=project,
            probability_of_delay__gte=0.50
        ).select_related('task').order_by('-probability_of_delay')[:5]

        risks = [
            {
                "task_id": p.task.id,
                "task_title": p.task.title,
                "delay_prob": p.probability_of_delay,
                "predicted_impact": "High" if p.probability_of_delay > 0.8 else "Medium"
            }
            for p in high_risk_predictions
        ]

        # 3. Upcoming Deadlines (Milestones & Tasks due in next 7 days)
        now = timezone.now().date()
        next_week = now + timezone.timedelta(days=7)

        upcoming_milestones = Milestone.objects.filter(
            project=project,
            due_date__range=[now, next_week]
        ).values("id", "name", "due_date")

        data = {
            "snapshot": snapshot,
            "active_risks": risks,
            "upcoming_deadlines": list(upcoming_milestones),
            "ai_recommendations": ["Consider re-assigning blocked tasks", "Update PERT estimates for Phase 2"] if project.health_score < 70 else ["System running optimally"],
        }

        return Response(data)


class ProjectTimelineAPIView(APIView):
    """
    Accepts Gantt JSON and computes timeline.
    """

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            gantt_json = request.data
            TimelinePlanningService(project).run(gantt_json)
            return Response({"message": "Timeline computed successfully"}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)