from django.urls import path
from .views import (
    ProjectListAPIView,
    ProjectTimelineAPIView,
    ProjectDashboardAPIView,
    ProjectContextAPIView
)

urlpatterns = [
    path('', ProjectListAPIView.as_view(), name='project-list'),
    path('context-list/', ProjectContextAPIView.as_view(), name='project-context-list'),
    path('<int:project_id>/dashboard/', ProjectDashboardAPIView.as_view(), name='project-dashboard'),
    path('<int:project_id>/timeline/', ProjectTimelineAPIView.as_view(), name='project-timeline'),
]