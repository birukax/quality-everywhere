from django.urls import path
from . import views

app_name = "machine"

urlpatterns = [
    path("list", views.list, name="list"),
    path("create", views.create, name="create"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("route/list", views.route_list, name="route_list"),
    path("route/create", views.create_route, name="create_route"),
    path("route/edit/<int:id>", views.edit_route, name="edit_route"),
    path(
        "route/<int:id>/update",
        views.update_machine_route,
        name="update_machine_route",
    ),
    path(
        "route/<int:id>/cancel",
        views.cancel_create_route,
        name="cancel_create_route",
    ),
]
