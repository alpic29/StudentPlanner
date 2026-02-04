import customtkinter as ctk


class SplashPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Student Planner", font=ctk.CTkFont(size=34, weight="bold"))
        title.grid(row=0, column=0, pady=(0, 10), sticky="s")

        self.status = ctk.CTkLabel(self, text="Loading...", font=ctk.CTkFont(size=14))
        self.status.grid(row=1, column=0, pady=(0, 10))

        self.progress = ctk.CTkProgressBar(self, width=320)
        self.progress.set(0)
        self.progress.grid(row=2, column=0, pady=(0, 60), sticky="n")

        # Fake loading animation
        self._p = 0.0
        self.after(250, self._tick)

    def _tick(self):
        self._p += 0.08
        if self._p >= 1.0:
            self.progress.set(1.0)
            self.status.configure(text="Ready")
            # small delay then move to login
            self.after(350, lambda: self.app.show_page("LoginPage"))
            return

        self.progress.set(self._p)
        self.after(120, self._tick)