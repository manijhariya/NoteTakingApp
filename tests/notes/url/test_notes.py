from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from notes.models import Note

AUTH_SAMPLE_DATA = {
    "username": "johnwick",
    "password": "aB@#2022",
    "email": "abc@xyz.com",
    "first_name": "John",
    "last_name": "Wick",
}


class NoteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(**AUTH_SAMPLE_DATA)
        self.note = Note.objects.create(
            title="Test Note", content="This is a test note.", owner=self.user
        )

    def test_create_note(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("create_note"),
            {"title": "New Note", "content": "This is a new note."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_create_note_no_title(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("create_note"),
            {"content": "This is a new note."},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid title", response.json()["error"])

    def test_create_note_no_content(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("create_note"),
            {"title": "New Note"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid content", response.json()["error"])


    def test_get_note(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("get_or_update_note", args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Test Note")

    def test_get_note_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("get_or_update_note", args=[3]))
        self.assertEqual(response.status_code, 404)

    def test_get_note_forbidden(self):
        ANOTHER_USER = {
            "username": "ethanhunt",
            "password": "aB@#2022",
            "email": "xyz@abc.com",
            "first_name": "Ethan",
            "last_name": "Hunt",
        }
        new_user = User.objects.create_user(**ANOTHER_USER)
        self.client.force_login(new_user)
        response = self.client.get(reverse("get_or_update_note", args=[self.note.id]))
        self.assertEqual(response.status_code, 403)


    def test_share_note(self):
        self.client.force_login(self.user)
        ANOTHER_USER = {
            "username": "ethanhunt",
            "password": "aB@#2022",
            "email": "xyz@abc.com",
            "first_name": "Ethan",
            "last_name": "Hunt",
        }

        new_user = User.objects.create_user(**ANOTHER_USER)
        response = self.client.post(
            reverse("share_note"),
            {"note_id": self.note.id, "usernames": [new_user.username]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(new_user in self.note.shared_with.all())

    def test_share_note_with_self(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("share_note"),
            {"note_id": self.note.id, "usernames": [self.user.username]},
        )
        self.assertEqual(response.status_code, 400)
    
    def test_share_note_with_already_shared(self):
        self.client.force_login(self.user)
        ANOTHER_USER = {
            "username": "ethanhunt",
            "password": "aB@#2022",
            "email": "xyz@abc.com",
            "first_name": "Ethan",
            "last_name": "Hunt",
        }

        new_user = User.objects.create_user(**ANOTHER_USER)
        response = self.client.post(
            reverse("share_note"),
            {"note_id": self.note.id, "usernames": [new_user.username]},
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("share_note"),
            {"note_id": self.note.id, "usernames": [new_user.username]},
        )
        self.assertEqual(response.status_code, 400)

    def test_update_note(self):
        self.client.force_login(self.user)
        response = self.client.put(
            reverse("get_or_update_note", args=[self.note.id]),
            {"content": "This is an updated note."},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertIn("This is an updated note.", self.note.content)

    def test_update_note_forbidden(self):
        ANOTHER_USER = {
            "username": "ethanhunt",
            "password": "aB@#2022",
            "email": "xyz@abc.com",
            "first_name": "Ethan",
            "last_name": "Hunt",
        }

        new_user = User.objects.create_user(**ANOTHER_USER)
        self.client.force_login(new_user)
        response = self.client.put(
            reverse("get_or_update_note", args=[self.note.id]),
            {"content": "This is an updated note."},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.note.refresh_from_db()
        self.assertIn("This is a test note.", self.note.content)

    def test_update_note_no_cotent(self):
        self.client.force_login(self.user)
        response = self.client.put(
            reverse("get_or_update_note", args=[self.note.id]),
            {},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.note.refresh_from_db()
        self.assertIn("This is a test note.", self.note.content)

    def test_get_note_history(self):
        self.client.force_login(self.user)
        response = self.client.put(
            reverse("get_or_update_note", args=[self.note.id]),
            {"content": "This is an updated note."},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("get_note_history", args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_get_note_history_no_update(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("get_note_history", args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_note_history_forbidden(self):
        ANOTHER_USER = {
            "username": "ethanhunt",
            "password": "aB@#2022",
            "email": "xyz@abc.com",
            "first_name": "Ethan",
            "last_name": "Hunt",
        }

        new_user = User.objects.create_user(**ANOTHER_USER)
        self.client.force_login(new_user)
        response = self.client.put(
            reverse("get_or_update_note", args=[self.note.id]),
            {"content": "This is an updated note."},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
