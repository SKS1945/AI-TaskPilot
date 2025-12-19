from django.urls import path
from task.views import (
    TaskListAPIView,
    AutoAssignTaskAPIView,
    MonitorProgressAPIView,
    PredictDelayAPIView,
)

urlpatterns = [
    path("<int:project_id>/", TaskListAPIView.as_view()),
    path("<int:project_id>/assign/", AutoAssignTaskAPIView.as_view()),
    path("<int:project_id>/monitor/", MonitorProgressAPIView.as_view()),
    path("<int:project_id>/predict/", PredictDelayAPIView.as_view()),
]
