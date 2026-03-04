import json
import os
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "schedule.json")
VALID_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class ScheduleService:
    def __init__(self):
        self.events = self._load_events()

    def _load_events(self):
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_events(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.events, file, indent=4)

    def get_all_events(self):
        day_index = {day: idx for idx, day in enumerate(VALID_DAYS)}
        return sorted(
            self.events,
            key=lambda event: (day_index.get(event["day"], 999), event["start_time"], event["course"]),
        )

    def add_event(self, course, day, start_time, end_time):
        course = course.strip()
        day = day.strip()
        start_time = start_time.strip()
        end_time = end_time.strip()

        if not course or not day or not start_time or not end_time:
            return False, "Fill in course, day, start time, and end time."
        if day not in VALID_DAYS:
            return False, "Day must be one of Monday-Sunday."

        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            return False, "Use 24-hour time format HH:MM (example: 13:30)."

        if end <= start:
            return False, "End time must be after start time."

        next_id = max([event["event_id"] for event in self.events], default=0) + 1
        self.events.append(
            {
                "event_id": next_id,
                "course": course,
                "day": day,
                "start_time": start_time,
                "end_time": end_time,
            }
        )
        self._save_events()
        return True, "Schedule event added."

    def delete_event(self, event_id):
        old_count = len(self.events)
        self.events = [event for event in self.events if event["event_id"] != event_id]
        if len(self.events) == old_count:
            return False, "Event ID not found."
        self._save_events()
        return True, "Schedule event deleted."
