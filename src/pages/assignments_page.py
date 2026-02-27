import customtkinter as ctk
from tkinter import messagebox


class AssignmentsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_task_id = None

        ctk.CTkLabel(self, text="Assignments", font=("Arial", 22, "bold")).pack(pady=10)

        form = ctk.CTkFrame(self)
        form.pack(padx=20, pady=10, fill="x")

        self.title_entry = ctk.CTkEntry(form, placeholder_text="Title")
        self.title_entry.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

        self.course_entry = ctk.CTkEntry(form, placeholder_text="Course (ex: CS36000)")
        self.course_entry.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

        self.date_entry = ctk.CTkEntry(form, placeholder_text="Due Date (YYYY-MM-DD)")
        self.date_entry.grid(row=0, column=2, padx=6, pady=6, sticky="ew")

        self.priority_entry = ctk.CTkEntry(form, placeholder_text="Priority (Low/Medium/High)")
        self.priority_entry.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        form.grid_columnconfigure(0, weight=2)
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(2, weight=1)
        form.grid_columnconfigure(3, weight=1)

        btns = ctk.CTkFrame(self)
        btns.pack(pady=5)

        ctk.CTkButton(btns, text="Add", command=self.add_task).grid(row=0, column=0, padx=6, pady=6)
        ctk.CTkButton(btns, text="Toggle Complete", command=self.toggle_complete).grid(row=0, column=1, padx=6, pady=6)
        ctk.CTkButton(btns, text="Delete", command=self.delete_task).grid(row=0, column=2, padx=6, pady=6)

        self.listbox = ctk.CTkTextbox(self, height=280)
        self.listbox.pack(fill="both", expand=True, padx=20, pady=10)
        self.listbox.configure(state="disabled")

        select_row = ctk.CTkFrame(self)
        select_row.pack(pady=5)

        ctk.CTkLabel(select_row, text="Task ID:").grid(row=0, column=0, padx=6)
        self.select_entry = ctk.CTkEntry(select_row, width=120, placeholder_text="ex: 1")
        self.select_entry.grid(row=0, column=1, padx=6)

        ctk.CTkButton(select_row, text="Select", command=self.select_task).grid(row=0, column=2, padx=6)

        self.stats_label = ctk.CTkLabel(self, text="")
        self.stats_label.pack(pady=5)

        self.refresh()

    def refresh(self):
        tasks = self.app.task_service.get_all_tasks()
        stats = self.app.task_service.get_progress()

        lines = []
        for t in tasks:
            status = "DONE" if t.completed else "TODO"
            lines.append(f"[{t.task_id}] {status} | {t.course} | {t.title} | due {t.due_date} | {t.priority}")

        self.listbox.configure(state="normal")
        self.listbox.delete("1.0", "end")
        self.listbox.insert("end", "\n".join(lines) if lines else "No tasks yet.")
        self.listbox.configure(state="disabled")

        self.stats_label.configure(
            text=f"Total: {stats['total']}   Done: {stats['done']}   Pending: {stats['pending']}"
        )

    def add_task(self):
        title = self.title_entry.get().strip()
        course = self.course_entry.get().strip()
        due_date = self.date_entry.get().strip()
        priority = (self.priority_entry.get().strip() or "Medium")

        if not title or not course or not due_date:
            messagebox.showerror("Error", "Fill in Title, Course, and Due Date.")
            return

        self.app.task_service.add_task(title, course, due_date, priority)
        self.title_entry.delete(0, "end")
        self.course_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.priority_entry.delete(0, "end")
        self.refresh()

    def select_task(self):
        raw = self.select_entry.get().strip()
        if not raw.isdigit():
            messagebox.showerror("Error", "Enter a numeric task id.")
            return
        self.selected_task_id = int(raw)
        messagebox.showinfo("Selected", f"Selected Task ID = {self.selected_task_id}")

    def toggle_complete(self):
        if self.selected_task_id is None:
            messagebox.showerror("Error", "Select a task id first.")
            return
        self.app.task_service.toggle_complete(self.selected_task_id)
        self.refresh()

    def delete_task(self):
        if self.selected_task_id is None:
            messagebox.showerror("Error", "Select a task id first.")
            return
        self.app.task_service.delete_task(self.selected_task_id)
        self.selected_task_id = None
        self.select_entry.delete(0, "end")
        self.refresh()
