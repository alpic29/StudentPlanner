import customtkinter as ctk
from pages.schedule_page import SchedulePage
from pages.assignments_page import AssignmentsPage

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_rowconfigure(10, weight=1)

        logo = ctk.CTkLabel(sidebar, text="Planner", font=ctk.CTkFont(size=20, weight="bold"))
        logo.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="w")

        btn_schedule = ctk.CTkButton(sidebar, text="Schedule", command=self._show_schedule)
        btn_schedule.grid(row=1, column=0, padx=16, pady=(8, 8), sticky="ew")

        btn_logout = ctk.CTkButton(sidebar, text="Log out", fg_color="#444", command=self._logout)
        btn_logout.grid(row=11, column=0, padx=16, pady=16, sticky="ew")

        # Content area
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Internal pages inside main
        btn_assignments = ctk.CTkButton(sidebar, text="Assignments", command=self._show_assignments)
        btn_assignments.grid(row=2, column=0, padx=16, pady=(8, 8), sticky="ew")
        self.schedule_page = SchedulePage(self.content)
        self.schedule_page.grid(row=0, column=0, sticky="nsew")

        self.assignments_page = AssignmentsPage(self.content, app)
        self.assignments_page.grid(row=0, column=0, sticky="nsew")

        self._show_schedule()
        
    def _show_schedule(self):
        self.schedule_page.tkraise()
        

    def _logout(self):
        self.app.show_page("LoginPage")

    def _show_assignments(self):
        self.assignments_page.refresh()
        self.assignments_page.tkraise()
       
