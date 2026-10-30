
from django import forms
from .models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "project",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
        ]

        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

        error_messages = {
            "project": {
                "required": "Please select a project.",
            },
            "title": {
                "required": "Please enter a task title.",
                "max_length": "Task title cannot exceed 200 characters.",
            },
            "status": {
                "invalid_choice": "Please select a valid task status.",
            },
            "priority": {
                "invalid_choice": "Please select a valid priority.",
            },
            "due_date": {
                "invalid": "Please enter a valid due date.",
            },
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["project"].queryset = (
            Project.objects.none()
            if user is None
            else Project.objects.filter(owner=user)
        )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

        error_messages = {
            "name": {
                "required": "Please enter a project name.",
                "max_length": "Project name cannot exceed 150 characters.",
            },
        }
