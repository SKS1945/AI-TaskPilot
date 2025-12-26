from task.models import Task, TaskDependency
from collections import defaultdict


def compute_pert(task):
    if not all([
        task.optimistic_hours,
        task.most_likely_hours,
        task.pessimistic_hours
    ]):
        return None, None

    expected = (
        task.optimistic_hours +
        4 * task.most_likely_hours +
        task.pessimistic_hours
    ) / 6

    variance = ((task.pessimistic_hours - task.optimistic_hours) / 6) ** 2
    return expected, variance


def build_task_graph(project):
    graph = defaultdict(list)
    for dep in TaskDependency.objects.filter(dependent_task__project=project):
        if dep.predecessor_task:
            graph[dep.predecessor_task.id].append(dep.dependent_task.id)
    return graph
