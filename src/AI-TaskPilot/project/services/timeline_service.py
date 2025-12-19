from datetime import datetime, timedelta
from collections import defaultdict, deque

from django.db import transaction
from django.utils.dateparse import parse_date

from project.models import TimelineSnapshot
from task.models import Task


class TimelinePlanningService:
    """
    Builds task schedule, critical path, and float values
    from a Gantt JSON structure.
    """

    def __init__(self, project):
        self.project = project
        self.tasks = {}
        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)
        self.duration = {}
        self.earliest_start = {}
        self.earliest_finish = {}
        self.latest_start = {}
        self.latest_finish = {}

    def load_from_gantt(self, gantt_json: dict):
        """
        Load task graph and durations from Gantt JSON.
        """
        for t in gantt_json.get("tasks", []):
            task = Task.objects.get(id=t["task_id"], project=self.project)
            self.tasks[t["id"]] = task
            self.duration[t["id"]] = t["duration"]

            for dep in t.get("dependencies", []):
                self.graph[dep].append(t["id"])
                self.reverse_graph[t["id"]].append(dep)

    def _topological_sort(self):
        indegree = defaultdict(int)
        for u in self.graph:
            for v in self.graph[u]:
                indegree[v] += 1

        queue = deque([n for n in self.tasks if indegree[n] == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in self.graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        return order

    def compute_early_times(self):
        order = self._topological_sort()

        for node in order:
            es = max(
                (self.earliest_finish[p] for p in self.reverse_graph[node]),
                default=0,
            )
            self.earliest_start[node] = es
            self.earliest_finish[node] = es + self.duration[node]

    def compute_late_times(self):
        project_duration = max(self.earliest_finish.values())
        order = reversed(self._topological_sort())

        for node in order:
            lf = min(
                (self.latest_start[c] for c in self.graph[node]),
                default=project_duration,
            )
            self.latest_finish[node] = lf
            self.latest_start[node] = lf - self.duration[node]

    @transaction.atomic
    def apply_schedule(self):
        """
        Write computed schedule back to Task models.
        """
        project_start = self.project.planned_start

        for gid, task in self.tasks.items():
            start = project_start + timedelta(days=self.earliest_start[gid])
            finish = project_start + timedelta(days=self.earliest_finish[gid])

            task.planned_start = start
            task.planned_finish = finish
            task.total_float_hours = (
                self.latest_start[gid] - self.earliest_start[gid]
            ) * 24
            task.is_on_critical_path = self.total_float(gid) == 0
            task.save(
                update_fields=[
                    "planned_start",
                    "planned_finish",
                    "total_float_hours",
                    "is_on_critical_path",
                ]
            )

    def total_float(self, node):
        return self.latest_start[node] - self.earliest_start[node]

    def persist_snapshot(self, gantt_json: dict):
        """
        Store immutable timeline snapshot.
        """
        TimelineSnapshot.objects.create(
            project=self.project,
            network_json={
                "earliest": self.earliest_start,
                "latest": self.latest_start,
            },
            gantt_json=gantt_json,
            summary={
                "critical_path": [
                    gid for gid in self.tasks if self.total_float(gid) == 0
                ],
                "project_duration_days": max(self.earliest_finish.values()),
            },
        )

    def run(self, gantt_json: dict):
        """
        Full pipeline.
        """
        self.load_from_gantt(gantt_json)
        self.compute_early_times()
        self.compute_late_times()
        self.apply_schedule()
        self.persist_snapshot(gantt_json)
