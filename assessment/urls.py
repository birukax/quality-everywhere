from django.urls import path
from . import views

app_name = "assessment"

urlpatterns = [
    path("list/<str:status>", views.list, name="list"),
    path("detail/<int:id>", views.detail, name="detail"),
    # path("edit/<int:id>", views.edit, name="edit"),
    # path("tests/save/<int:id>", views.save_tests, name="save_tests"),
    path("first-off/create/<int:id>", views.create_first_off, name="create_first_off"),
    path("test/list", views.test_list, name="test_list"),
    path("test/create", views.create_test, name="create_test"),
    path("test/<int:id>/edit", views.edit_test, name="edit_test"),
    path("conformity/list", views.conformity_list, name="conformity_list"),
    path("conformity/create", views.create_conformity, name="create_conformity"),
    path("conformity/<int:id>/edit", views.edit_conformity, name="edit_conformity"),
]
