from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("compare/", views.compare, name="compare"),
    path("school/<int:unit_id>/", views.school_detail, name="school_detail"),
]