from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Evaluation, Guide, Project
from .permissions import ROLE_GUIDE, ROLE_STUDENT, assign_role


class RoleBasedAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student_user = User.objects.create_user(username="student1", password="pass12345")
        assign_role(cls.student_user, ROLE_STUDENT)

        cls.other_student = User.objects.create_user(username="student2", password="pass12345")
        assign_role(cls.other_student, ROLE_STUDENT)

        cls.guide_user = User.objects.create_user(username="guide1", password="pass12345")
        assign_role(cls.guide_user, ROLE_GUIDE)
        cls.guide = Guide.objects.create(name="Guide One", user=cls.guide_user)

        cls.admin_user = User.objects.create_superuser(
            username="admin1",
            password="pass12345",
            email="admin@example.com",
        )

        cls.student_project = Project.objects.create(
            title="Smart Attendance",
            domain="AI",
            student1_name="Student One",
            student1_usn="USN001",
            student2_name="Student Mate",
            student2_usn="USN002",
            created_by=cls.student_user,
            guide=cls.guide,
        )
        cls.other_project = Project.objects.create(
            title="Water Tracker",
            domain="IoT",
            student1_name="Student Two",
            student1_usn="USN003",
            student2_name="Student Peer",
            student2_usn="USN004",
            created_by=cls.other_student,
        )

    def test_auth_selection_page_has_role_links(self):
        response = self.client.get(reverse("auth_selection"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you a Student or a Guide?")
        self.assertContains(response, reverse("role_auth", args=["student"]))
        self.assertContains(response, reverse("role_auth", args=["guide"]))

    def test_student_can_register_project_and_ownership_is_saved(self):
        self.client.force_login(self.student_user)

        response = self.client.post(
            reverse("register"),
            {
                "title": "Campus Connect",
                "domain": "Web",
                "student1_name": "Student One",
                "student1_usn": "USN101",
                "student2_name": "Student Two",
                "student2_usn": "USN102",
                "student3_name": "",
                "student3_usn": "",
                "student4_name": "",
                "student4_usn": "",
            },
        )

        self.assertRedirects(response, reverse("register"))
        project = Project.objects.get(title="Campus Connect")
        self.assertEqual(project.created_by, self.student_user)

    def test_student_can_access_register_and_upload_but_not_evaluate(self):
        self.client.force_login(self.student_user)

        register_response = self.client.get(reverse("register"))
        upload_response = self.client.get(reverse("upload"))
        evaluate_response = self.client.get(reverse("evaluate"))

        self.assertEqual(register_response.status_code, 200)
        self.assertEqual(upload_response.status_code, 200)
        self.assertRedirects(evaluate_response, reverse("home"))
        self.assertQuerySetEqual(
            upload_response.context["form"].fields["project"].queryset,
            [self.student_project],
            transform=lambda project: project,
        )

    def test_guide_cannot_access_student_features(self):
        self.client.force_login(self.guide_user)

        register_response = self.client.get(reverse("register"))
        upload_response = self.client.get(reverse("upload"))

        self.assertRedirects(register_response, reverse("home"))
        self.assertRedirects(upload_response, reverse("home"))

    def test_guide_only_sees_assigned_projects_in_evaluation_form(self):
        self.client.force_login(self.guide_user)

        response = self.client.get(reverse("evaluate"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["form"].fields["project"].queryset,
            [self.student_project],
            transform=lambda project: project,
        )

    def test_student_project_list_is_scoped_to_owned_projects(self):
        self.client.force_login(self.student_user)

        response = self.client.get(reverse("projects_list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["projects"],
            [self.student_project],
            transform=lambda project: project,
        )

    def test_admin_can_access_admin_features(self):
        self.client.force_login(self.admin_user)

        allot_response = self.client.get(reverse("allot", args=[self.student_project.id]))
        export_response = self.client.get(reverse("export_csv"))

        self.assertEqual(allot_response.status_code, 200)
        self.assertEqual(export_response.status_code, 200)
        self.assertEqual(export_response["Content-Type"], "text/csv")

    def test_role_login_rejects_wrong_group(self):
        self.client.logout()

        response = self.client.post(
            reverse("role_auth", args=["student"]),
            {
                "auth_action": "login",
                "login-username": "guide1",
                "login-password": "pass12345",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "not registered as a student")

    def test_guide_reuses_existing_evaluation_for_assigned_project(self):
        evaluation = Evaluation.objects.create(
            project=self.student_project,
            guide_rating="Good",
            marks=70,
            comments="Initial review",
            evaluated_by=self.guide_user,
        )
        self.client.force_login(self.guide_user)

        response = self.client.post(
            reverse("evaluate"),
            {
                "project": self.student_project.id,
                "guide_rating": "Excellent",
                "marks": 88,
                "comments": "Improved after revision",
                "publication_status": "on",
            },
        )

        self.assertRedirects(response, reverse("evaluate"))
        evaluation.refresh_from_db()
        self.assertEqual(Evaluation.objects.filter(project=self.student_project).count(), 1)
        self.assertEqual(evaluation.marks, 88)
        self.assertEqual(evaluation.guide_rating, "Excellent")
