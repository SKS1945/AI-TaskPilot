from skill.models import ResourceSkill


def compute_skill_match(resource, task):
    required_skills = task.metadata.get("required_skills", [])
    if not required_skills:
        return 1.0

    skills = ResourceSkill.objects.filter(resource=resource)
    skill_map = {s.skill.name: s.proficiency_level for s in skills}

    matched = 0
    for rs in required_skills:
        if rs in skill_map:
            matched += skill_map[rs]

    return matched / (len(required_skills) * 5)
