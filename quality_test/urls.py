from django.urls import path, include
from . import views

app_name = "quality_test"

urlpatterns = [
    path("list/<str:status>", views.list, name="list"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("tests/save/<int:id>", views.save_tests, name="save_tests"),
]
