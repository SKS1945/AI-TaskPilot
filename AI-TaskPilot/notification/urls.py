from django.urls import path
from notification.views import EvaluateNotificationsAPIView

urlpatterns = [
    path(
        'projects/<int:project_id>/notifications/evaluate/',
        EvaluateNotificationsAPIView.as_view()
    ),
]
