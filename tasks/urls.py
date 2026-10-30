
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/create/", views.create_project, name="create_project"),
    path(
        "projects/<int:project_id>/delete/",
        views.delete_project,
        name="delete_project",
    ),
    path(
    "projects/<int:project_id>/edit/",
    views.edit_project,
    name="edit_project",
),
    path("tasks/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
]
