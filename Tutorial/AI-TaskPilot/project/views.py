from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from task.services.timeline import build_gantt_for_project
from project.services.timeline import save_timeline_snapshot
from project.serializers import TimelineSnapshotSerializer


class ProjectTimelineAPIView(APIView):
    """
    POST /api/projects/{project_id}/timeline/
    GET  /api/projects/{project_id}/timeline/latest/
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)

        gantt_data = build_gantt_for_project(project)
        snapshot = save_timeline_snapshot(project, gantt_data)

        serializer = TimelineSnapshotSerializer(snapshot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, project_id):
        snapshot = (
            Project.objects
            .get(id=project_id)
            .timeline_snapshots
            .order_by('-created_at')
            .first()
        )

        if not snapshot:
            return Response(
                {"error": "No timeline found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TimelineSnapshotSerializer(snapshot)
        return Response(serializer.data)


from task.services.cpm import compute_cpm
from project.services.timeline import save_cpm_snapshot


class ProjectCPMAPIView(APIView):
    """
    POST /api/projects/{project_id}/cpm/
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)

        cpm_result = compute_cpm(project)

        # reuse existing gantt
        snapshot = project.timeline_snapshots.order_by('-created_at').first()
        if not snapshot:
            return Response(
                {"error": "Generate timeline before CPM"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_snapshot = save_cpm_snapshot(
            project,
            snapshot.gantt_json,
            cpm_result
        )

        serializer = TimelineSnapshotSerializer(new_snapshot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



from rest_framework.views import APIView
from rest_framework.response import Response

from project.models import Project
from project.services.risk import compute_project_delay_risk


class ProjectDelayRiskAPIView(APIView):
    """
    GET /api/projects/{project_id}/delay-risk/
    """

    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        risk_data = compute_project_delay_risk(project)
        return Response(risk_data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from project.services.weekly_planner import generate_weekly_planner


class WeeklyPlannerAPIView(APIView):
    """
    GET /api/projects/{project_id}/weekly-planner/?week_start=YYYY-MM-DD
    """

    def get(self, request, project_id):
        week_start = request.query_params.get("week_start")
        if not week_start:
            return Response(
                {"error": "week_start query param required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        project = Project.objects.get(id=project_id)
        planner = generate_weekly_planner(project, datetime.fromisoformat(week_start).date())

        return Response(planner)
