from project.models import ProjectReport


def generate_project_report(project, report_type, payload, summary):
    return ProjectReport.objects.create(
        project=project,
        report_type=report_type,
        payload=payload,
        summary=summary
    )
