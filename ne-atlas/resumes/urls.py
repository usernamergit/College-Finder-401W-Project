from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.resume_preview, name="resume_preview"),
]