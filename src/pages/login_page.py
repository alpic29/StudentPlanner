import customtkinter as ctk


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(self, corner_radius=16)
        card.grid(row=0, column=0, padx=24, pady=24)

        title = ctk.CTkLabel(card, text="Welcome back", font=ctk.CTkFont(size=24, weight="bold"))
        subtitle = ctk.CTkLabel(card, text="Log in to continue", font=ctk.CTkFont(size=14))
        title.grid(row=0, column=0, columnspan=2, padx=24, pady=(24, 4), sticky="w")
        subtitle.grid(row=1, column=0, columnspan=2, padx=24, pady=(0, 16), sticky="w")

        self.email = ctk.CTkEntry(card, width=320, placeholder_text="Email or username")
        self.password = ctk.CTkEntry(card, width=320, placeholder_text="Password", show="•")
        self.email.grid(row=2, column=0, columnspan=2, padx=24, pady=(0, 10))
        self.password.grid(row=3, column=0, columnspan=2, padx=24, pady=(0, 8))

        self.error = ctk.CTkLabel(card, text="", text_color="#ff6b6b")
        self.error.grid(row=4, column=0, columnspan=2, padx=24, pady=(0, 6), sticky="w")

        login_btn = ctk.CTkButton(card, text="Log in", width=320, command=self._login)
        login_btn.grid(row=5, column=0, columnspan=2, padx=24, pady=(6, 10))

        signup_link = ctk.CTkButton(
            card,
            text="Create an account",
            fg_color="transparent",
            hover=False,
            text_color=("#1f6feb", "#4ea1ff"),
            command=lambda: self.app.show_page("SignupPage"),
        )
        signup_link.grid(row=6, column=0, columnspan=2, padx=24, pady=(0, 24))

        # Enter key to login
        self.password.bind("<Return>", lambda _e: self._login())

    def _login(self):
        email = self.email.get().strip()
        pw = self.password.get().strip()

        ok, message = self.app.auth_service.login(email, pw)
        if not ok:
            self.error.configure(text=message)
            return

        self.error.configure(text="")
        self.app.show_page("MainPage")
