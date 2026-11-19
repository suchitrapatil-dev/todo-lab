from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="task_list"),                       # /tasks/
    path("new/", views.task_create, name="task_create"),               # /tasks/new/
    path("<int:pk>/", views.task_detail, name="task_detail"),          # /tasks/5/
    path("<int:pk>/edit/", views.task_update, name="task_update"),     # /tasks/5/edit/
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),   # /tasks/5/delete/
]
