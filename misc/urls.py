from django.urls import path
from . import views

app_name = "misc"

urlpatterns = [
    path("customer/list", views.customer_list, name="customer_list"),
    path("customer/get", views.get_customers, name="get_customers"),
    path("raw_material/list", views.raw_material_list, name="raw_material_list"),
    path("raw_material/create", views.create_raw_material, name="create_raw_material"),
    path(
        "raw_material/<int:id>/edit", views.edit_raw_material, name="edit_raw_material"
    ),
    path("shift/list", views.shift_list, name="shift_list"),
    path("shift/create", views.create_shift, name="create_shift"),
    path("shift/<int:id>/edit", views.edit_shift, name="edit_shift"),
    path("color/list", views.color_list, name="color_list"),
    path("color/create", views.create_color, name="create_color"),
    path("color/<int:id>/edit", views.edit_color, name="edit_color"),
    path("color_standard/list", views.color_standard_list, name="color_standard_list"),
    path(
        "color_standard/create",
        views.create_color_standard,
        name="create_color_standard",
    ),
    path(
        "color_standard/<int:id>/edit",
        views.edit_color_standard,
        name="edit_color_standard",
    ),
]
