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
        self.confirm = ctk.CTkEntry(card, width=320, placeholder_text="Confirm Password", show="•")
        self.email.grid(row=2, column=0, padx=24, pady=(0, 10))
        self.password.grid(row=3, column=0, padx=24, pady=(0, 10))
        self.confirm.grid(row=4, column=0, padx=24, pady=(0, 10))

        create_btn = ctk.CTkButton(card, text="Create", width=320, command=self._create)
        create_btn.grid(row=5, column=0, padx=24, pady=(6, 10))

        back_btn = ctk.CTkButton(
            card,
            text="Back to login",
            fg_color="transparent",
            hover=False,
            text_color=("#1f6feb", "#4ea1ff"),
            command=lambda: self.app.show_page("LoginPage"),
        )
        back_btn.grid(row=6, column=0, padx=24, pady=(0, 24))

        self.msg = ctk.CTkLabel(card, text="")
        self.msg.grid(row=7, column=0, padx=24, pady=(0, 18), sticky="w")

    def _create(self):
        email = self.email.get().strip()
        password = self.password.get().strip()
        confirm = self.confirm.get().strip()

        if password != confirm:
            self.msg.configure(text="Passwords do not match.", text_color="#ff6b6b")
            return

        ok, message = self.app.auth_service.register(email, password)
        self.msg.configure(text=message, text_color="#7bd88f" if ok else "#ff6b6b")
        if not ok:
            return

        self.email.delete(0, "end")
        self.password.delete(0, "end")
        self.confirm.delete(0, "end")
        self.after(700, lambda: self.app.show_page("LoginPage"))
