from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snippet, Tag

User = get_user_model()


class SnipBoxAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )

        # Login user
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )

        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_create_snippet(self):
        data = {
            "title": "Test Snippet",
            "note": "This is a test",
            "tags": ["django", "api"],
        }

        response = self.client.post("/api/snippets/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)

    def test_snippet_overview(self):
        Snippet.objects.create(title="Overview Test", note="Test", created_by=self.user)

        response = self.client.get("/api/snippets/overview/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_snippets"], 1)

    def test_snippet_detail_owner_only(self):
        snippet = Snippet.objects.create(
            title="Detail Test", note="Test", created_by=self.user
        )

        response = self.client.get(f"/api/snippets/{snippet.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_detail_forbidden_for_other_user(self):
        snippet = Snippet.objects.create(
            title="Forbidden Test", note="Test", created_by=self.other_user
        )

        response = self.client.get(f"/api/snippets/{snippet.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_snippet(self):
        snippet = Snippet.objects.create(
            title="Old Title", note="Old note", created_by=self.user
        )

        data = {"title": "Updated Title", "note": "Updated note", "tags": ["updated"]}

        response = self.client.put(f"/api/snippets/{snippet.id}/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snippet.refresh_from_db()
        self.assertEqual(snippet.title, "Updated Title")

    def test_delete_snippet(self):
        snippet = Snippet.objects.create(
            title="Delete Test", note="Test", created_by=self.user
        )

        response = self.client.delete(f"/api/snippets/{snippet.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)

    def test_tag_list(self):
        Tag.objects.create(title="django")
        response = self.client.get("/api/tags/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_detail(self):
        tag = Tag.objects.create(title="django")
        snippet = Snippet.objects.create(
            title="Tagged", note="Test", created_by=self.user
        )
        snippet.tags.add(tag)

        response = self.client.get(f"/api/tags/{tag.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
