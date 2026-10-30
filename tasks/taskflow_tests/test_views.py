
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from tasks.models import Project, Task


class ProjectViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="projectuser",
            password="testpassword123",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123",
        )

        self.project = Project.objects.create(
            owner=self.user,
            name="My Project",
            description="Project description",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_logged_in_user(self):
        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Project")

    def test_user_only_sees_own_projects(self):
        Project.objects.create(
            owner=self.other_user,
            name="Other User Project",
        )

        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, "My Project")
        self.assertNotContains(response, "Other User Project")

    def test_create_project(self):
        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("create_project"),
            {
                "name": "New Project",
                "description": "Created through a test",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))

        project = Project.objects.get(name="New Project")
        self.assertEqual(project.owner, self.user)

    def test_edit_nonexistent_project_returns_404(self):
        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse("edit_project", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_project_returns_404(self):
        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("delete_project", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_project(self):
        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("edit_project", args=[self.project.id]),
            {
                "name": "Updated Project",
                "description": "Updated description",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))

        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")

    def test_user_cannot_edit_another_users_project(self):
        self.client.login(
            username="otheruser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse("edit_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_view_another_users_project(self):
        self.client.login(
            username="otheruser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse(
                "edit_project",
                args=[self.project.id],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_project(self):
        task = Task.objects.create(
            project=self.project,
            title="Project Task",
        )

        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("delete_project", args=[self.project.id])
        )

        self.assertRedirects(response, reverse("dashboard"))

        self.assertFalse(
            Project.objects.filter(id=self.project.id).exists()
        )

        self.assertFalse(
            Task.objects.filter(id=task.id).exists()
        )

    def test_user_cannot_delete_another_users_project(self):
        self.client.login(
            username="otheruser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Project.objects.filter(id=self.project.id).exists()
        )

    def test_delete_project_get_does_not_delete_project(self):
        self.client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse("delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Project.objects.filter(id=self.project.id).exists()
        )

    def test_delete_project_without_csrf_token_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)

        csrf_client.login(
            username="projectuser",
            password="testpassword123",
        )

        response = csrf_client.post(
            reverse("delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Project.objects.filter(id=self.project.id).exists()
        )


class TaskViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="taskuser",
            password="testpassword123",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123",
        )

        self.project = Project.objects.create(
            owner=self.user,
            name="My Task Project",
        )

        self.other_project = Project.objects.create(
            owner=self.other_user,
            name="Other User Project",
        )

        self.task = Task.objects.create(
            project=self.project,
            title="Original Task",
            description="Original description",
            status=Task.Status.TODO,
            priority=Task.Priority.MEDIUM,
        )

    def test_create_task(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("dashboard"),
            {
                "project": self.project.id,
                "title": "New Task",
                "description": "Created through a test",
                "status": "TODO",
                "priority": "HIGH",
                "due_date": "",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))

        task = Task.objects.get(title="New Task")
        self.assertEqual(task.project, self.project)

    def test_user_cannot_create_task_for_another_users_project(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("dashboard"),
            {
                "project": self.other_project.id,
                "title": "Unauthorized Task",
                "description": "",
                "status": "TODO",
                "priority": "MEDIUM",
                "due_date": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Task.objects.filter(title="Unauthorized Task").exists()
        )

    def test_edit_nonexistent_task_returns_404(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse("edit_task", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_task_returns_404(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("delete_task", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_edit_task(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("edit_task", args=[self.task.id]),
            {
                "project": self.project.id,
                "title": "Updated Task",
                "description": "Updated description",
                "status": "IN_PROGRESS",
                "priority": "HIGH",
                "due_date": "",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)

    def test_user_cannot_edit_another_users_task(self):
        self.client.login(
            username="otheruser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse("edit_task", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("delete_task", args=[self.task.id])
        )

        self.assertRedirects(response, reverse("dashboard"))

        self.assertFalse(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_user_cannot_delete_another_users_task(self):
        self.client.login(
            username="otheruser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("delete_task", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_delete_task_get_does_not_delete_task(self):
        self.client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = self.client.get(
            reverse("delete_task", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_delete_task_without_csrf_token_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)

        csrf_client.login(
            username="taskuser",
            password="testpassword123",
        )

        response = csrf_client.post(
            reverse("delete_task", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Task.objects.filter(id=self.task.id).exists()
        )
