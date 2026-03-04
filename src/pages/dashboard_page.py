import customtkinter as ctk
from datetime import datetime


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w", padx=24, pady=(18, 12))

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", padx=24)
        cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.total_card = self._card(cards, "Total Tasks")
        self.total_card.grid(row=0, column=0, padx=6, sticky="ew")
        self.done_card = self._card(cards, "Completed Tasks")
        self.done_card.grid(row=0, column=1, padx=6, sticky="ew")
        self.upcoming_card = self._card(cards, "Upcoming Deadlines")
        self.upcoming_card.grid(row=0, column=2, padx=6, sticky="ew")
        self.progress_card = self._card(cards, "Progress %")
        self.progress_card.grid(row=0, column=3, padx=6, sticky="ew")

        deadlines_box = ctk.CTkFrame(self)
        deadlines_box.pack(fill="both", expand=True, padx=24, pady=(16, 20))
        ctk.CTkLabel(
            deadlines_box,
            text="Next Due Assignments",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.deadlines_text = ctk.CTkTextbox(deadlines_box, height=220)
        self.deadlines_text.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.deadlines_text.configure(state="disabled")

    def _card(self, parent, label):
        frame = ctk.CTkFrame(parent)
        value = ctk.CTkLabel(frame, text="0", font=ctk.CTkFont(size=26, weight="bold"))
        value.pack(pady=(14, 4))
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=13)).pack(pady=(0, 14))
        frame.value_label = value
        return frame

    def refresh(self):
        tasks = self.app.task_service.get_all_tasks()
        total = len(tasks)
        done = len([task for task in tasks if task.completed])
        pending = [task for task in tasks if not task.completed]
        progress = int((done / total) * 100) if total else 0

        def parse_date(task):
            try:
                return datetime.strptime(task.due_date, "%Y-%m-%d")
            except ValueError:
                return None

        today = datetime.today().date()
        upcoming = [task for task in pending if parse_date(task) and parse_date(task).date() >= today]
        upcoming_sorted = sorted(upcoming, key=lambda task: parse_date(task))
        nearest = upcoming_sorted[:5]

        self.total_card.value_label.configure(text=str(total))
        self.done_card.value_label.configure(text=str(done))
        self.upcoming_card.value_label.configure(text=str(len(upcoming)))
        self.progress_card.value_label.configure(text=f"{progress}%")

        lines = []
        for task in nearest:
            lines.append(f"{task.due_date}  |  {task.course}  |  {task.title}  |  {task.priority}")

        self.deadlines_text.configure(state="normal")
        self.deadlines_text.delete("1.0", "end")
        self.deadlines_text.insert("end", "\n".join(lines) if lines else "No upcoming deadlines.")
        self.deadlines_text.configure(state="disabled")
