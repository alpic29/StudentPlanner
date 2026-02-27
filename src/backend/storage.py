import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
