from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from notification.models import Notification
from notification.services.notification_service import NotificationEvaluationService


class RunNotificationEngineAPIView(APIView):
    """
    Evaluates notification rules and generates notifications.
    """

    def post(self, request):
        generated = NotificationEvaluationService().run()
        return Response(
            {"notifications_generated": len(generated)},
            status=status.HTTP_200_OK
        )


class NotificationListAPIView(APIView):
    def get(self, request):
        notifications = Notification.objects.all().values(
            "id", "target_type", "status", "generated_at", "content"
        )
        return Response(list(notifications))
