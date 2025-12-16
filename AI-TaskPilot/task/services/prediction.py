import random
from task.models import TaskPrediction


def monte_carlo_delay_probability(task, iterations=1000):
    delays = 0

    for _ in range(iterations):
        duration = random.triangular(
            float(task.optimistic_hours),
            float(task.pessimistic_hours),
            float(task.most_likely_hours)
        )
        if duration > float(task.expected_hours):
            delays += 1

    probability = delays / iterations

    return TaskPrediction.objects.create(
        task=task,
        model_name="MonteCarlo-PERT",
        probability_of_delay=round(probability, 4),
        details={"iterations": iterations}
    )
