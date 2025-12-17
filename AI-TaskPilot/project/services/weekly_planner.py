from datetime import timedelta
from django.utils.timezone import make_aware
from django.utils.timezone import datetime

from task.models import TaskAssignment
from resource.models import ResourceAvailability


WEEKLY_CAPACITY_HOURS = 40


def generate_weekly_planner(project, week_start_date):
    """
    week_start_date: date (Monday)
    """
    week_start = make_aware(
        datetime.combine(week_start_date, datetime.min.time())
    )
    week_end = week_start + timedelta(days=6)

    assignments = (
        TaskAssignment.objects
        .filter(task__project=project)
        .select_related('task', 'resource')
    )

    planner = {}

    for assignment in assignments:
        task = assignment.task
        resource = assignment.resource

        # Skip tasks not active this week
        if not task.planned_start or not task.planned_finish:
            continue

        if task.planned_finish < week_start or task.planned_start > week_end:
            continue

        planner.setdefault(resource.id, {
            "resource_id": resource.id,
            "resource_name": resource.display_name,
            "tasks": [],
            "total_allocated_hours": 0
        })

        allocated = float(assignment.allocated_effort or 0)

        planner[resource.id]["tasks"].append({
            "task_id": task.id,
            "title": task.title,
            "planned_start": task.planned_start.date(),
            "planned_finish": task.planned_finish.date(),
            "allocated_hours": allocated,
            "is_critical": task.is_on_critical_path
        })

        planner[resource.id]["total_allocated_hours"] += allocated

    # Evaluate overload
    for r in planner.values():
        r["overloaded"] = r["total_allocated_hours"] > WEEKLY_CAPACITY_HOURS

    return {
        "week_start": week_start.date(),
        "week_end": week_end.date(),
        "resources": list(planner.values())
    }
