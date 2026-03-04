import json
import os
import tempfile
import unittest

from src.services import auth_service, schedule_service


class TestMatiasServices(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.auth_file = os.path.join(self.tmpdir.name, "users.json")
        self.schedule_file = os.path.join(self.tmpdir.name, "schedule.json")
        with open(self.auth_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(self.schedule_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        self.original_auth_file = auth_service.DATA_FILE
        self.original_schedule_file = schedule_service.DATA_FILE
        auth_service.DATA_FILE = self.auth_file
        schedule_service.DATA_FILE = self.schedule_file

    def tearDown(self):
        auth_service.DATA_FILE = self.original_auth_file
        schedule_service.DATA_FILE = self.original_schedule_file
        self.tmpdir.cleanup()

    def test_register_and_login_success(self):
        service = auth_service.AuthService()
        ok, _ = service.register("matias@example.com", "secret1")
        self.assertTrue(ok)

        ok, _ = service.login("matias@example.com", "secret1")
        self.assertTrue(ok)

    def test_register_duplicate_fails(self):
        service = auth_service.AuthService()
        service.register("matias@example.com", "secret1")
        ok, message = service.register("matias@example.com", "secret2")
        self.assertFalse(ok)
        self.assertIn("already exists", message)

    def test_schedule_add_and_delete(self):
        service = schedule_service.ScheduleService()
        ok, _ = service.add_event("CS 180", "Monday", "09:00", "10:15")
        self.assertTrue(ok)
        self.assertEqual(len(service.get_all_events()), 1)

        ok, _ = service.delete_event(1)
        self.assertTrue(ok)
        self.assertEqual(len(service.get_all_events()), 0)


if __name__ == "__main__":
    unittest.main()
