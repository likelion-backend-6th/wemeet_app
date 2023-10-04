from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Plan


class PlanViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.plan = Plan.objects.create(
            title="Test Plan", description="This is a test plan.", owner=self.user
        )

    def test_plan_list_view(self):
        response = self.client.get(reverse("plan-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plan/plan_list.html")
        self.assertContains(response, "Test Plan")

        response = self.client.get(reverse("plan-detail", args=[self.plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plan/plan_detail.html")
        self.assertContains(response, "Test Plan")

    def test_plan_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("plan-create"),
            {
                "title": "New Test Plan",
                "description": "This is a new test plan.",
                "owner": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("plan-list"))
        self.assertTrue(Plan.objects.filter(title="New Test Plan").exists())
