from collections import defaultdict, deque
from datetime import timedelta

from task.models import Task, TaskDependency


def _duration_days(task):
    if task.expected_hours:
        return max(1, int(task.expected_hours // 8))
    return 1


def compute_cpm(project):
    """
    Computes:
    - ES, EF
    - LS, LF
    - Total Float
    - Critical Path
    """

    tasks = Task.objects.filter(project=project)
    deps = TaskDependency.objects.filter(dependent_task__project=project)

    # Build graph
    successors = defaultdict(list)
    predecessors = defaultdict(list)

    for d in deps:
        if d.predecessor_task:
            successors[d.predecessor_task.id].append(d.dependent_task.id)
            predecessors[d.dependent_task.id].append(d.predecessor_task.id)

    task_map = {t.id: t for t in tasks}

    # ---------- FORWARD PASS ----------
    ES = {}
    EF = {}

    topo_queue = deque()
    in_degree = {t.id: 0 for t in tasks}

    for t_id, preds in predecessors.items():
        in_degree[t_id] = len(preds)

    for t_id, deg in in_degree.items():
        if deg == 0:
            topo_queue.append(t_id)
            ES[t_id] = 0
            EF[t_id] = _duration_days(task_map[t_id])

    topo_order = []

    while topo_queue:
        current = topo_queue.popleft()
        topo_order.append(current)

        for succ in successors[current]:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                ES[succ] = max(EF[p] for p in predecessors[succ])
                EF[succ] = ES[succ] + _duration_days(task_map[succ])
                topo_queue.append(succ)

    project_duration = max(EF.values()) if EF else 0

    # ---------- BACKWARD PASS ----------
    LS = {}
    LF = {}

    for t_id in reversed(topo_order):
        if t_id not in successors or not successors[t_id]:
            LF[t_id] = project_duration
        else:
            LF[t_id] = min(LS[s] for s in successors[t_id])

        LS[t_id] = LF[t_id] - _duration_days(task_map[t_id])

    # ---------- FLOAT + CRITICAL ----------
    for t_id, task in task_map.items():
        total_float = LS[t_id] - ES[t_id]

        task.total_float_hours = total_float * 8
        task.is_on_critical_path = total_float == 0

        task.planned_start = project.planned_start + timedelta(days=ES[t_id])
        task.planned_finish = project.planned_start + timedelta(days=EF[t_id])

        task.save(update_fields=[
            'total_float_hours',
            'is_on_critical_path',
            'planned_start',
            'planned_finish'
        ])

    return {
        "project_duration_days": project_duration,
        "critical_tasks": [
            t.id for t in task_map.values() if t.is_on_critical_path
        ]
    }
