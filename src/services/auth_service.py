import json
import os


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")


class AuthService:
    def __init__(self):
        self.users = self._load_users()

    def _load_users(self):
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_users(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=4)

    def register(self, email, password):
        email = email.strip().lower()
        password = password.strip()

        if not email or not password:
            return False, "Email and password are required."
        if "@" not in email or "." not in email:
            return False, "Please enter a valid email."
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        if any(user["email"] == email for user in self.users):
            return False, "An account with this email already exists."

        self.users.append({"email": email, "password": password})
        self._save_users()
        return True, "Account created successfully."

    def login(self, email, password):
        email = email.strip().lower()
        password = password.strip()

        if not email or not password:
            return False, "Please enter both email and password."

        for user in self.users:
            if user["email"] == email and user["password"] == password:
                return True, "Login successful."

        return False, "Invalid email or password."
