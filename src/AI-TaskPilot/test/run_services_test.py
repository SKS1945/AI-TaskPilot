import json
from pathlib import Path

from project.services.timeline_service import TimelinePlanningService
from task.services.assignment_service import SmartAssignmentService
from task.services.progress_monitoring_service import ProgressMonitoringService
from task.services.delay_prediction_service import DelayPredictionService
from notification.services.notification_service import NotificationEvaluationService
from project.models import Project


BASE = Path(__file__).parent / "data"


def run():
    project = Project.objects.get(key="AI-TP-01")

    gantt = json.loads((BASE / "gantt.json").read_text())

    TimelinePlanningService(project).run(gantt)
    SmartAssignmentService(project).run()
    ProgressMonitoringService(project).run()
    DelayPredictionService(project).run()
    NotificationEvaluationService().run()

    print("All services executed successfully")
