from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from project.services.timeline_service import TimelinePlanningService


class ProjectListAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all().values(
            "id", "key", "name", "status", "health_score"
        )
        return Response(list(projects))


class ProjectTimelineAPIView(APIView):
    """
    Accepts Gantt JSON and computes timeline.
    """

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        gantt_json = request.data

        TimelinePlanningService(project).run(gantt_json)

        return Response(
            {"message": "Timeline computed successfully"},
            status=status.HTTP_200_OK
        )
