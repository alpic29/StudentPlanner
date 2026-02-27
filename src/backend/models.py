from dataclasses import dataclass

@dataclass
class Task:
    task_id: int
    title: str
    course: str
    due_date: str
    completed: bool = False
    priority: str = "Medium"
