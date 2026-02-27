from backend.models import Task
from backend.storage import load_tasks, save_tasks

class TaskService:
    def __init__(self):
        self.tasks = self._load()

    def _load(self):
        raw_tasks = load_tasks()
        return [Task(**task) for task in raw_tasks]

    def _save(self):
        save_tasks([task.__dict__ for task in self.tasks])

    def get_all_tasks(self):
        return self.tasks

    def add_task(self, title, course, due_date, priority="Medium"):
        task_id = len(self.tasks) + 1
        task = Task(task_id, title, course, due_date, False, priority)
        self.tasks.append(task)
        self._save()
        return task

    def toggle_complete(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = not task.completed
        self._save()

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self._save()

    def get_progress(self):
        total = len(self.tasks)
        done = len([t for t in self.tasks if t.completed])
        return {
            "total": total,
            "done": done,
            "pending": total - done
        }
