from django.urls import path
from task.views import AutoAssignTaskAPIView

urlpatterns = [
    path('tasks/<int:task_id>/assign/', AutoAssignTaskAPIView.as_view()),
]
