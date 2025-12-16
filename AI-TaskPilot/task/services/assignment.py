from task.models import TaskAssignment
from resource.services.availability import get_latest_availability
from skill.services.matching import compute_skill_match


def score_resource(resource, task):
    availability = get_latest_availability(resource)
    skill_match = compute_skill_match(resource, task)

    if not availability:
        return -1

    return (
        0.5 * skill_match -
        0.3 * availability['load_factor'] +
        0.2 * availability['availability_ratio']
    )


def assign_best_resource(task, resources):
    best_score = float('-inf')
    best_resource = None

    for resource in resources:
        score = score_resource(resource, task)
        if score > best_score:
            best_score = score
            best_resource = resource

    if best_resource:
        return TaskAssignment.objects.create(
            task=task,
            resource=best_resource,
            allocated_effort=task.expected_hours or 0
        )
