from django.shortcuts import render, redirect
from .models import Project, Task
from .forms import TaskForm
from django.shortcuts import render, redirect, get_object_or_404

def dashboard(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm()

    projects = Project.objects.all()
    tasks = Task.objects.select_related("project").all()

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

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {"form": form, "task": task},
    )


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("dashboard")

    return render(
        request,
        "tasks/delete_task.html",
        {"task": task},
    )