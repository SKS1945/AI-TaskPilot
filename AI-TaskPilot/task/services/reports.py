from task.models import TaskReport


def generate_task_report(task, report_type, payload, summary):
    return TaskReport.objects.create(
        task=task,
        report_type=report_type,
        payload=payload,
        summary=summary
    )
