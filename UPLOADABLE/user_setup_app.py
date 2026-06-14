"""
UPLOADABLE - User Input Template App
Allows a new user to input their information after downloading the project.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox

class UploadableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JobGoblin - User Setup")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Enter your email settings:", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(frame, text="SMTP Host:").pack(anchor="w")
        self.smtp_host = ttk.Entry(frame)
        self.smtp_host.pack(fill="x", pady=2)

        ttk.Label(frame, text="SMTP Port:").pack(anchor="w")
        self.smtp_port = ttk.Entry(frame)
        self.smtp_port.pack(fill="x", pady=2)

        ttk.Label(frame, text="SMTP User:").pack(anchor="w")
        self.smtp_user = ttk.Entry(frame)
        self.smtp_user.pack(fill="x", pady=2)

        ttk.Label(frame, text="SMTP Password:").pack(anchor="w")
        self.smtp_password = ttk.Entry(frame, show="*")
        self.smtp_password.pack(fill="x", pady=2)

        ttk.Button(frame, text="Save Settings", command=self.save_settings).pack(pady=10)

    def save_settings(self):
        settings = {
            "SMTP_HOST": self.smtp_host.get(),
            "SMTP_PORT": self.smtp_port.get(),
            "SMTP_USER": self.smtp_user.get(),
            "SMTP_PASSWORD": self.smtp_password.get()
        }
        with open(".env", "w") as f:
            for k, v in settings.items():
                f.write(f"{k}={v}\n")
        messagebox.showinfo("Saved", "SMTP settings saved to .env file.")

if __name__ == "__main__":
    app = UploadableApp()
    app.mainloop()
