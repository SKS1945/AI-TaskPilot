from task.models import TaskProgress


def record_progress(task, percent, effort, note=""):
    return TaskProgress.objects.create(
        task=task,
        percent_complete=percent,
        effort_consumed=effort,
        status_note=note
    )
