from task.models import TaskAssignment


def current_workload(resource):
    assignments = TaskAssignment.objects.filter(resource=resource)
    return sum(a.allocated_effort for a in assignments)
