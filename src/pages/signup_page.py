import customtkinter as ctk


class SignupPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(self, corner_radius=16)
        card.grid(row=0, column=0, padx=24, pady=24)

        title = ctk.CTkLabel(card, text="Create account", font=ctk.CTkFont(size=24, weight="bold"))
        subtitle = ctk.CTkLabel(card, text="This can be mocked for now", font=ctk.CTkFont(size=14))
        title.grid(row=0, column=0, padx=24, pady=(24, 4), sticky="w")
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="w")

        self.email = ctk.CTkEntry(card, width=320, placeholder_text="Email")
        self.password = ctk.CTkEntry(card, width=320, placeholder_text="Password", show="•")
        self.email.grid(row=2, column=0, padx=24, pady=(0, 10))
        self.password.grid(row=3, column=0, padx=24, pady=(0, 10))

        create_btn = ctk.CTkButton(card, text="Create", width=320, command=self._create)
        create_btn.grid(row=4, column=0, padx=24, pady=(6, 10))

        back_btn = ctk.CTkButton(
            card,
            text="Back to login",
            fg_color="transparent",
            hover=False,
            text_color=("#1f6feb", "#4ea1ff"),
            command=lambda: self.app.show_page("LoginPage"),
        )
        back_btn.grid(row=5, column=0, padx=24, pady=(0, 24))

        self.msg = ctk.CTkLabel(card, text="")
        self.msg.grid(row=6, column=0, padx=24, pady=(0, 18), sticky="w")

    def _create(self):
        # Mock signup
        self.msg.configure(text="Account created (mock). Returning to login...")
        self.after(900, lambda: self.app.show_page("LoginPage"))