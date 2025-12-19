from django.urls import path
from project.views import ProjectListAPIView, ProjectTimelineAPIView

urlpatterns = [
    path("", ProjectListAPIView.as_view()),
    path("<int:project_id>/timeline/", ProjectTimelineAPIView.as_view()),
]
