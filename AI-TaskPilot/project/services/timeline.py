from project.models import TimelineSnapshot
from task.models import Task, TaskDependency


def create_timeline_snapshot(project, network, gantt, summary):
    """
    Stores computed AON + Gantt snapshot
    """
    return TimelineSnapshot.objects.create(
        project=project,
        network_json=network,
        gantt_json=gantt,
        summary=summary
    )
