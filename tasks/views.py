
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

    # Get projects belonging to the logged-in user
    projects = Project.objects.filter(owner=request.user)

    # Get tasks belonging to the logged-in user's projects
    all_tasks = Task.objects.filter(
        project__owner=request.user
    ).select_related("project")

    # Read selected filters from the URL
    selected_status = request.GET.get("status", "")
    selected_priority = request.GET.get("priority", "")
    selected_project = request.GET.get("project", "")
    search_query = request.GET.get("search", "").strip()

    # Start with all tasks
    tasks = all_tasks
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Apply status filter
    valid_statuses = [
        choice[0] for choice in Task.Status.choices
    ]

    if selected_status in valid_statuses:
        tasks = tasks.filter(status=selected_status)
    else:
        selected_status = ""

    # Apply priority filter
    valid_priorities = [
        choice[0] for choice in Task.Priority.choices
    ]

    if selected_priority in valid_priorities:
        tasks = tasks.filter(priority=selected_priority)
    else:
        selected_priority = ""

    # Filter by project
    if selected_project.isdigit():
        tasks = tasks.filter(project_id=int(selected_project))
    else:
        selected_project = ""

    # Dashboard statistics
    context = {
        "projects": projects,
        "tasks": tasks,
        "total_tasks": all_tasks.count(),
        "completed_tasks": all_tasks.filter(
            status=Task.Status.DONE
        ).count(),
        "form": form,
        "selected_status": selected_status,
        "status_choices": Task.Status.choices,
        "selected_priority": selected_priority,
        "priority_choices": Task.Priority.choices,
        "selected_project": selected_project,
        "search_query": search_query
    }

    return render(
        request,
        "tasks/dashboard.html",
        context,
    )


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
        {"form": form},
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
        form = ProjectForm(
            request.POST,
            instance=project,
        )

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
