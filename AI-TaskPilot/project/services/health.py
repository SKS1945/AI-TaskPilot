from task.models import Task


def compute_project_health(project):
    tasks = Task.objects.filter(project=project)
    if not tasks.exists():
        project.health_score = 100
        project.save()
        return 100

    total_weight = sum(t.weight for t in tasks)
    weighted_health = 0

    for task in tasks:
        progress = task.progress_entries.order_by('-snapshot_time').first()
        if progress:
            weighted_health += task.weight * float(progress.percent_complete)

    project.health_score = round(weighted_health / total_weight, 2)
    project.save()
    return project.health_score
