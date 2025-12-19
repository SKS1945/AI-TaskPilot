import json
from pathlib import Path
from django.utils.dateparse import parse_date

from skill.models import Skill
from resource.models import Resource
from skill.models import ResourceSkill
from project.models import Project
from task.models import Task, TaskProgress
from notification.models import NotificationRule


BASE = Path(__file__).parent / "data"


def load_json(name):
    with open(BASE / name) as f:
        return json.load(f)


def run():
    # Skills
    for s in load_json("skills.json")["skills"]:
        Skill.objects.get_or_create(**s)

    # Resources
    for r in load_json("resources.json")["resources"]:
        res = Resource.objects.create(
            display_name=r["display_name"],
            email=r["email"],
            capacity_hours_per_week=r["capacity_hours_per_week"],
        )
        for sk in r["skills"]:
            ResourceSkill.objects.create(
                resource=res,
                skill=Skill.objects.get(name=sk["name"]),
                proficiency_level=sk["level"],
            )

    # Project
    p = load_json("project.json")
    project = Project.objects.create(
        key=p["key"],
        name=p["name"],
        description=p["description"],
        status=p["status"],
        planned_start=parse_date(p["planned_start"]),
        planned_finish=parse_date(p["planned_finish"]),
    )

    # Tasks
    tasks = []
    for t in load_json("tasks.json")["tasks"]:
        tasks.append(Task.objects.create(project=project, **t))

    # Progress
    for pr in load_json("progress.json")["progress"]:
        TaskProgress.objects.create(
            task=tasks[pr["task_index"]],
            percent_complete=pr["percent_complete"],
            effort_consumed=pr["effort_consumed"],
        )

    # Notification rules
    for r in load_json("notification_rules.json")["rules"]:
        NotificationRule.objects.create(**r)

    print("Sample data loaded successfully")
