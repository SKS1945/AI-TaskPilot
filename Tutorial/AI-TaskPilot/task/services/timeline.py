from datetime import timedelta
from django.utils.timezone import make_aware
from task.models import Task, TaskDependency


def build_gantt_for_project(project):
    tasks = Task.objects.filter(project=project)
    dependencies = TaskDependency.objects.filter(dependent_task__project=project)

    gantt_tasks = []
    gantt_links = []

    # Basic scheduling: sequential fallback
    current_date = project.planned_start

    for task in tasks.order_by('id'):
        if task.planned_start:
            start = task.planned_start
        else:
            start = current_date

        duration = int(task.expected_hours or 8) // 8 or 1
        end = start + timedelta(days=duration)

        task.planned_start = start
        task.planned_finish = end
        task.save(update_fields=['planned_start', 'planned_finish'])

        progress = 0
        latest = task.progress_entries.order_by('-snapshot_time').first()
        if latest:
            progress = float(latest.percent_complete) / 100

        gantt_tasks.append({
            "id": task.id,
            "text": task.title,
            "start_date": start.strftime("%Y-%m-%d"),
            "duration": duration,
            "progress": round(progress, 2),
            "open": True
        })

        current_date = end

    link_id = 1
    for dep in dependencies:
        if dep.predecessor_task:
            gantt_links.append({
                "id": link_id,
                "source": dep.predecessor_task.id,
                "target": dep.dependent_task.id,
                "type": "0"   # Finish-to-start
            })
            link_id += 1

    return {
        "data": gantt_tasks,
        "links": gantt_links
    }
