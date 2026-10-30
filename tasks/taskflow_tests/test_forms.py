
from django.test import TestCase
from django.contrib.auth.models import User

from tasks.models import Project
from tasks.forms import ProjectForm, TaskForm


class ProjectFormTests(TestCase):

    def test_valid_project_form(self):
        form = ProjectForm(data={
            "name": "My Project",
            "description": "Testing project form",
        })

        self.assertTrue(form.is_valid())

    def test_project_form_requires_name(self):
        form = ProjectForm(data={
            "name": "",
            "description": "Testing project form",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


    def test_project_name_max_length(self):
        form = ProjectForm(data={
            "name": "A" * 151,
            "description": "Testing maximum length",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_project_description_is_optional(self):
        form = ProjectForm(data={
            "name": "Project Without Description",
            "description": "",
        })

        self.assertTrue(form.is_valid())

class TaskFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="formuser",
            password="testpassword123",
        )

        self.project = Project.objects.create(
            owner=self.user,
            name="User Project",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpassword123",
        )

        self.other_project = Project.objects.create(
            owner=self.other_user,
            name="Other Project",
        )

    def test_task_form_only_shows_users_projects(self):
        form = TaskForm(user=self.user)

        project_choices = list(
            form.fields["project"].queryset
        )

        self.assertIn(self.project, project_choices)
        self.assertNotIn(self.other_project, project_choices)

    def test_task_form_valid_data(self):
        form = TaskForm(
            data={
                "project": self.project.id,
                "title": "Test Task",
                "description": "Testing task form",
                "status": "TODO",
                "priority": "MEDIUM",
                "due_date": "",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_requires_title(self):
        form = TaskForm(
            data={
                "project": self.project.id,
                "title": "",
                "description": "",
                "status": "TODO",
                "priority": "MEDIUM",
                "due_date": "",
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        
        
    def test_task_title_max_length(self):
        form = TaskForm(
            data={
                "project": self.project.id,
                "title": "A" * 201,
                "description": "",
                "status": "TODO",
                "priority": "MEDIUM",
                "due_date": "",
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_task_form_rejects_invalid_status(self):
        form = TaskForm(
            data={
                "project": self.project.id,
                "title": "Test Task",
                "description": "",
                "status": "INVALID",
                "priority": "MEDIUM",
                "due_date": "",
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)

    def test_task_form_rejects_invalid_priority(self):
        form = TaskForm(
            data={
                "project": self.project.id,
                "title": "Test Task",
                "description": "",
                "status": "TODO",
                "priority": "URGENT",
                "due_date": "",
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)

