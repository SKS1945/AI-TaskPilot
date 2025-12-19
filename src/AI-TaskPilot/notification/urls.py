from django.urls import path
from notification.views import RunNotificationEngineAPIView, NotificationListAPIView

urlpatterns = [
    path("run/", RunNotificationEngineAPIView.as_view()),
    path("", NotificationListAPIView.as_view()),
]
