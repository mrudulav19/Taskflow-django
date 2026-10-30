
from django.test import TestCase
from django.contrib.auth.models import User

from tasks.models import Project, Task


class ProjectModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.project = Project.objects.create(
            owner=self.user,
            name="Test Project",
            description="A project for testing"
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.owner, self.user)

    def test_project_string_representation(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_owner_relationship(self):
        self.assertEqual(
            self.user.projects.first(),
            self.project
        )


class TaskModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="taskuser",
            password="testpassword123"
        )

        self.project = Project.objects.create(
            owner=self.user,
            name="Task Test Project"
        )

        self.task = Task.objects.create(
            project=self.project,
            title="Test Task",
            description="Testing task creation"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.project, self.project)

    def test_task_default_status(self):
        self.assertEqual(
            self.task.status,
            Task.Status.TODO
        )

    def test_task_default_priority(self):
        self.assertEqual(
            self.task.priority,
            Task.Priority.MEDIUM
        )

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_project_deletion_deletes_tasks(self):
        self.project.delete()

        self.assertFalse(
            Task.objects.filter(id=self.task.id).exists()
        )
