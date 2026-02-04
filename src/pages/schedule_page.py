import customtkinter as ctk


class SchedulePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="Schedule (coming next)", font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(pady=(30, 8))

        desc = ctk.CTkLabel(
            self,
            text="Weekly view grid + add/edit events will go here.",
            font=ctk.CTkFont(size=14),
        )
        desc.pack(pady=(0, 20))