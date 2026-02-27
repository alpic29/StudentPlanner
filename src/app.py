import customtkinter as ctk

from pages.splash_page import SplashPage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.main_page import MainPage
from backend.task_service import TaskService

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")  # "light" or "system"
        ctk.set_default_color_theme("blue")

        self.title("Student Planner")
        self.geometry("1000x650")
        self.minsize(900, 600)

        # Container that holds pages
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        self.pages = {}

        for Page in (SplashPage, LoginPage, SignupPage, MainPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, app=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Start at splash
        self.show_page("SplashPage")

    def show_page(self, page_name: str):
        frame = self.pages[page_name]
        frame.tkraise()
