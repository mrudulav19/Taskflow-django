from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tasks/<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
]