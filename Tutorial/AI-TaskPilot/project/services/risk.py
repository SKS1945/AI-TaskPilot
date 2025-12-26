from task.models import Task, TaskPrediction


CRITICAL_MULTIPLIER = 1.5


def compute_project_delay_risk(project):
    tasks = Task.objects.filter(project=project)

    if not tasks.exists():
        return {
            "project_delay_probability": 0.0,
            "risk_score": 0.0,
            "top_risk_tasks": []
        }

    total_weight = 0.0
    weighted_risk_sum = 0.0
    task_risks = []

    for task in tasks:
        prediction = (
            task.predictions
            .order_by('-generated_at')
            .first()
        )

        if not prediction:
            continue

        weight = task.weight or 1
        multiplier = CRITICAL_MULTIPLIER if task.is_on_critical_path else 1.0

        task_risk = float(prediction.probability_of_delay) * weight * multiplier

        weighted_risk_sum += task_risk
        total_weight += weight

        task_risks.append({
            "task_id": task.id,
            "task_title": task.title,
            "probability": float(prediction.probability_of_delay),
            "is_critical": task.is_on_critical_path,
            "weight": weight,
            "risk_contribution": round(task_risk, 4)
        })

    project_delay_probability = (
        weighted_risk_sum / total_weight if total_weight > 0 else 0.0
    )

    risk_score = round(project_delay_probability * 100, 2)

    top_risk_tasks = sorted(
        task_risks,
        key=lambda x: x["risk_contribution"],
        reverse=True
    )[:5]

    return {
        "project_delay_probability": round(project_delay_probability, 4),
        "risk_score": risk_score,
        "top_risk_tasks": top_risk_tasks
    }
