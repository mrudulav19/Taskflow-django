
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Project, Task
from .forms import TaskForm, ProjectForm


@login_required
def dashboard(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(user=request.user)

    projects = Project.objects.filter(owner=request.user)

    tasks = Task.objects.filter(
        project__owner=request.user
    ).select_related("project")

    context = {
        "projects": projects,
        "tasks": tasks,
        "total_tasks": tasks.count(),
        "completed_tasks": tasks.filter(
            status=Task.Status.DONE
        ).count(),
        "form": form,
    }

    return render(request, "tasks/dashboard.html", context)


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("dashboard")
    else:
        form = ProjectForm()

    return render(
        request,
        "tasks/create_project.html",
        {"form": form}
    )


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        project__owner=request.user,
    )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            instance=task,
            user=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(
            instance=task,
            user=request.user,
        )

    return render(
        request,
        "tasks/edit_task.html",
        {"form": form, "task": task},
    )


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        project__owner=request.user,
    )

    if request.method == "POST":
        task.delete()
        return redirect("dashboard")

    return render(
        request,
        "tasks/delete_task.html",
        {"task": task},
    )

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user,
    )

    if request.method == "POST":
        project.delete()
        return redirect("dashboard")

    return render(
        request,
        "tasks/delete_project.html",
        {"project": project},
    )

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user,
    )

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "tasks/edit_project.html",
        {"form": form, "project": project},
    )
