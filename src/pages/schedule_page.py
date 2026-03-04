import customtkinter as ctk
from tkinter import messagebox


class SchedulePage(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.app = app
        self.selected_event_id = None

        title = ctk.CTkLabel(self, text="Schedule", font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(anchor="w", padx=20, pady=(16, 8))

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=20, pady=(0, 8))
        form.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.course_entry = ctk.CTkEntry(form, placeholder_text="Course Name (ex: CS 180)")
        self.course_entry.grid(row=0, column=0, padx=6, pady=8, sticky="ew")
        self.day_menu = ctk.CTkOptionMenu(
            form,
            values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        )
        self.day_menu.grid(row=0, column=1, padx=6, pady=8, sticky="ew")
        self.start_entry = ctk.CTkEntry(form, placeholder_text="Start Time (HH:MM)")
        self.start_entry.grid(row=0, column=2, padx=6, pady=8, sticky="ew")
        self.end_entry = ctk.CTkEntry(form, placeholder_text="End Time (HH:MM)")
        self.end_entry.grid(row=0, column=3, padx=6, pady=8, sticky="ew")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(0, 8))
        ctk.CTkButton(actions, text="Add Class", command=self.add_event).pack(side="left", padx=(0, 8))
        ctk.CTkButton(actions, text="Delete Selected", command=self.delete_event).pack(side="left")

        select_row = ctk.CTkFrame(self, fg_color="transparent")
        select_row.pack(fill="x", padx=20, pady=(0, 8))
        ctk.CTkLabel(select_row, text="Event ID:").pack(side="left")
        self.select_entry = ctk.CTkEntry(select_row, width=100, placeholder_text="ex: 1")
        self.select_entry.pack(side="left", padx=8)
        ctk.CTkButton(select_row, text="Select", command=self.select_event, width=90).pack(side="left")

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(anchor="w", padx=20, pady=(0, 4))

        self.events_box = ctk.CTkTextbox(self, height=320)
        self.events_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.events_box.configure(state="disabled")

        self.refresh()

    def refresh(self):
        events = self.app.schedule_service.get_all_events()
        lines = ["[ID] Day | Time | Course", "-------------------------------"]
        for event in events:
            lines.append(
                f"[{event['event_id']}] {event['day']} | {event['start_time']}-{event['end_time']} | {event['course']}"
            )

        self.events_box.configure(state="normal")
        self.events_box.delete("1.0", "end")
        self.events_box.insert("end", "\n".join(lines) if events else "No schedule events yet.")
        self.events_box.configure(state="disabled")

    def add_event(self):
        course = self.course_entry.get().strip()
        day = self.day_menu.get().strip()
        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()

        ok, message = self.app.schedule_service.add_event(course, day, start_time, end_time)
        self.msg.configure(text=message, text_color="#7bd88f" if ok else "#ff6b6b")
        if not ok:
            return

        self.course_entry.delete(0, "end")
        self.start_entry.delete(0, "end")
        self.end_entry.delete(0, "end")
        self.refresh()

    def select_event(self):
        raw = self.select_entry.get().strip()
        if not raw.isdigit():
            messagebox.showerror("Error", "Enter a numeric event id.")
            return
        self.selected_event_id = int(raw)
        messagebox.showinfo("Selected", f"Selected Event ID = {self.selected_event_id}")

    def delete_event(self):
        if self.selected_event_id is None:
            messagebox.showerror("Error", "Select an event id first.")
            return

        ok, message = self.app.schedule_service.delete_event(self.selected_event_id)
        self.msg.configure(text=message, text_color="#7bd88f" if ok else "#ff6b6b")
        if not ok:
            return

        self.selected_event_id = None
        self.select_entry.delete(0, "end")
        self.refresh()
