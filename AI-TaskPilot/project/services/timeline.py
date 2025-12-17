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



from project.models import TimelineSnapshot


def save_timeline_snapshot(project, gantt_data):
    return TimelineSnapshot.objects.create(
        project=project,
        network_json={},        # placeholder (CPM later)
        gantt_json=gantt_data,
        summary={
            "task_count": len(gantt_data["data"]),
            "generated_by": "basic_scheduler"
        }
    )


def save_cpm_snapshot(project, gantt_data, cpm_summary):
    return TimelineSnapshot.objects.create(
        project=project,
        network_json=cpm_summary,
        gantt_json=gantt_data,
        summary={
            "critical_path_task_ids": cpm_summary["critical_tasks"],
            "project_duration_days": cpm_summary["project_duration_days"],
            "generated_by": "cpm_engine"
        }
    )
