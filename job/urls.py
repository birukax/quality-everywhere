from django.urls import path, include
from . import views

app_name = "job"

urlpatterns = [
    path("list", views.list, name="list"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("create-first-off/<int:id>", views.create_first_off, name="create_first_off"),
]
