from django.urls import path
from . import views

app_name = "misc"

urlpatterns = [
    path("machine/list", views.machine_list, name="machine_list"),
    path("machine/create", views.create_machine, name="create_machine"),
    path("machine/<int:id>/edit", views.edit_machine, name="edit_machine"),
    path("customer/list", views.customer_list, name="customer_list"),
    path("customer/get", views.get_customers, name="get_customers"),
    path("product/list", views.product_list, name="product_list"),
    path("product/get", views.get_products, name="get_products"),
    path("paper/list", views.paper_list, name="paper_list"),
    path("paper/create", views.create_paper, name="create_paper"),
    path("paper/<int:id>/edit", views.edit_paper, name="edit_paper"),
    path("shift/list", views.shift_list, name="shift_list"),
    path("shift/create", views.create_shift, name="create_shift"),
    path("shift/<int:id>/edit", views.edit_shift, name="edit_shift"),
    path("test/list", views.test_list, name="test_list"),
    path("color/list", views.color_list, name="color_list"),
    path("color_standard/list", views.color_standard_list, name="color_standard_list"),
]
