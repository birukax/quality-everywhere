from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("list", views.list, name="list"),
    path("profile", views.profile, name="profile"),
    path("update", views.update, name="update"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("create", views.create, name="create"),
]
