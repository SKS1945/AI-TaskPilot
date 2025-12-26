from django.urls import path
from project.views import ProjectTimelineAPIView

urlpatterns = [
    path('projects/<int:project_id>/timeline/', ProjectTimelineAPIView.as_view()),
]

from project.views import ProjectCPMAPIView

urlpatterns += [
    path('projects/<int:project_id>/cpm/', ProjectCPMAPIView.as_view()),
]


from project.views import ProjectDelayRiskAPIView

urlpatterns += [
    path(
        'projects/<int:project_id>/delay-risk/',
        ProjectDelayRiskAPIView.as_view()
    ),
]
from project.views import WeeklyPlannerAPIView

urlpatterns += [
    path(
        'projects/<int:project_id>/weekly-planner/',
        WeeklyPlannerAPIView.as_view()
    ),
]
