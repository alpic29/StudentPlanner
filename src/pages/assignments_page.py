import customtkinter as ctk
from backend.task_service import TaskService

class AssignmentsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.task_service = app.task_service

        title = ctk.CTkLabel(self, text="Assignments", font=("Arial", 24))
        title.pack(pady=10)

        self.task_box = ctk.CTkTextbox(self, width=500, height=300)
        self.task_box.pack(pady=10)

        self.refresh()

    def refresh(self):
        self.task_box.delete("1.0", "end")
        tasks = self.task_service.get_all_tasks()
        for task in tasks:
            status = "✔" if task.completed else "✘"
            self.task_box.insert("end", f"{task.task_id} | {task.title} | {status}\n")
