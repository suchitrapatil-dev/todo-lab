from django.db import models
from django.urls import reverse


class Todo(models.Model):
    """One task in the shared Todo list (Activity 2)."""

    title = models.CharField(max_length=150)                 # required, max 150
    description = models.TextField(blank=True)               # optional
    completed = models.BooleanField(default=False)           # default False
    created_at = models.DateTimeField(auto_now_add=True)     # set automatically

    class Meta:
        # Ordering decision: newest tasks first, applied everywhere.
        ordering = ["-created_at"]

    def __str__(self):
        status = "done" if self.completed else "not done"
        return f"{self.title} ({status})"

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.pk})
