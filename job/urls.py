from django.urls import path, include
from . import views

app_name = "job"

urlpatterns = [
    path("jobs/get", views.get_jobs, name="get_jobs"),
    path("list", views.list, name="list"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("test/list", views.test_list, name="test_list"),
    path("test/detail/<int:id>", views.test_detail, name="test_detail"),
    path("test/next-machine/<int:id>", views.next_machine, name="next_machine"),
    # path("test/edit/<int:id>", views.test_edit, name="test_edit"),
    path("test/create/<int:id>", views.create_test, name="create_test"),
    path(
        "test/semi-waste/create/<int:id>",
        views.create_semi_waste,
        name="create_semi_waste",
    ),
]
