from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),            # Activity 3: include app URLs
    path("", RedirectView.as_view(pattern_name="tasks:task_list", permanent=False)),
]
