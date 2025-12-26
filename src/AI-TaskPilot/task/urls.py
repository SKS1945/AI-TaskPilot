from django.urls import path
from .views import (
    TaskListAPIView,
    TaskDetailAPIView,
    AutoAssignTaskAPIView,
    MonitorProgressAPIView,
    PredictDelayAPIView
)

urlpatterns = [
    path('project/<int:project_id>/', TaskListAPIView.as_view(), name='task-list'),
    path('<int:task_id>/', TaskDetailAPIView.as_view(), name='task-detail'),

    # AI Actions
    path('project/<int:project_id>/auto-assign/', AutoAssignTaskAPIView.as_view(), name='auto-assign'),
    path('project/<int:project_id>/monitor/', MonitorProgressAPIView.as_view(), name='monitor-progress'),
    path('project/<int:project_id>/predict-delay/', PredictDelayAPIView.as_view(), name='predict-delay'),
]