from django.urls import reverse
from django.test import TestCase
from .models import Plan, Group
from django.contrib.auth.models import User


class PlanViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="main", password="testpassword")
        self.client.login(username="main", password="testpassword")
        self.plan_data = {
            "owner": self.user,
            "title": "main title",
            "time": "2023-09-30T12:00:00Z",
            "latitude": "37.5575",
            "longitude": "126.9245",
            "memo": "main memo",
        }
        self.plan = Plan.objects.create(**self.plan_data)
        self.user2 = User.objects.create_user(username="user2", password="testpassword")

    # 생성된 plan 개수 비교
    def test_create_plan(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("plan_create"), format="json")
        self.assertEqual(Plan.objects.count(), 1)

    # title 변경 후 비교
    def test_update_plan(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("plan_edit", args=[self.plan.id]),
            {
                "title": "new title",
            },
        )
        print(response.status_code)
        self.plan.refresh_from_db()
        expected_url = reverse('plan_edit')

        self.assertEqual(self.plan.title, "new title")

    def test_delete_plan(self):
        # 권한 없는 유저가 삭제 시 실패
        self.client.force_login(self.user2)
        response = self.client.post(reverse("plan_delete", args=[self.plan.id]))
        self.assertEqual(Plan.objects.filter(owner=self.user).count(), 1)

        # 자신 plan 삭제
        self.client.force_login(self.user)
        response = self.client.post(reverse("plan_delete", args=[self.plan.id]))
        self.assertEqual(Plan.objects.filter(owner=self.user).count(), 0)
