from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from task.serializers import TaskAssignmentSerializer
from task.services.assignment_service import SmartAssignmentService



class AutoAssignTaskAPIView(APIView):
    """
    POST /api/tasks/{task_id}/assign/
    """

    def post(self, request, task_id):
        try:
            assignment = auto_assign_task(task_id)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskAssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
