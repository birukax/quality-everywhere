from django.urls import path
from . import views

app_name = "assessment"

urlpatterns = [
    path("first-off/create/<int:id>", views.create_first_off, name="create_first_off"),
    path("first-off/add/<int:id>", views.add_first_off, name="add_first_off"),
    path("first-off/list/<str:status>", views.first_off_list, name="first_off_list"),
    path("first-off/detail/<int:id>", views.first_off_detail, name="first_off_detail"),
    path("first-off/edit/<int:id>", views.edit_first_off, name="edit_first_off"),
    path("first-off/test/save/<int:id>", views.save_test, name="save_test"),
    path(
        "on-proces/create/<int:id>", views.create_on_process, name="create_on_process"
    ),
    path("on-process/list/<str:status>", views.on_process_list, name="on_process_list"),
    path(
        "on-process/detail/<int:id>", views.on_process_detail, name="on_process_detail"
    ),
    path("on-process/edit/<int:id>", views.edit_on_process, name="edit_on_process"),
    path(
        "on-process/conformity/save/<int:id>",
        views.save_conformity,
        name="save_conformity",
    ),
    path("test/list", views.test_list, name="test_list"),
    path("test/create", views.create_test, name="create_test"),
    path("test/<int:id>/edit", views.edit_test, name="edit_test"),
    path("conformity/list", views.conformity_list, name="conformity_list"),
    path("conformity/create", views.create_conformity, name="create_conformity"),
    path("conformity/<int:id>/edit", views.edit_conformity, name="edit_conformity"),
    path("waste/save/<int:id>", views.create_waste, name="create_waste"),
    path("waste/list", views.waste_list, name="waste_list"),
    path("semi-waste/list", views.semi_waste_list, name="semi_waste_list"),
    path(
        "semi-waste/update/<int:id>", views.update_semi_waste, name="update_semi_waste"
    ),
    path("viscosity/save/<int:id>", views.save_viscosity, name="save_viscosity"),
    path(
        "substrate/update/<int:id>", views.update_substrates, name="update_substrates"
    ),
]
