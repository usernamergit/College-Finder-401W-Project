from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("resume/", include("resumes.urls")),
    path("jobs/", include("jobs.urls")),
    path("", include("catalog.urls")),
]