from django.shortcuts import get_object_or_404, redirect, render

from .forms import TodoForm
from .models import Todo


def task_list(request):
    """READ: show all tasks (Activity 3)."""
    tasks = Todo.objects.all()  # ordering comes from Meta (newest first)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_detail(request, pk):
    """READ: show one task. 404 if it doesn't exist."""
    task = get_object_or_404(Todo, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


def task_create(request):
    """CREATE: GET shows empty form, POST validates and saves (Activity 4)."""
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect("tasks:task_detail", pk=task.pk)
        # invalid -> fall through and redisplay form with errors + entered values
    else:
        form = TodoForm()
    return render(request, "tasks/task_form.html", {"form": form, "is_edit": False})


def task_update(request, pk):
    """UPDATE: prefill with current values; bind POST to SAME instance (Activity 5)."""
    task = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=task)  # instance= means update, not insert
        if form.is_valid():
            form.save()
            return redirect("tasks:task_detail", pk=task.pk)
    else:
        form = TodoForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "task": task, "is_edit": True})


def task_delete(request, pk):
    """DELETE: GET only confirms; POST actually deletes (Activity 6)."""
    task = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("tasks:task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
