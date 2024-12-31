from django.urls import path
from . import views

app_name = 'misc'

urlpatterns = [
    path('machine/list', views.machine_list, name='machine_list'),
    path('customer/list', views.customer_list, name='customer_list'),
    path('product/list', views.product_list, name='product_list'),
    path('paper/list', views.paper_list, name='paper_list'),
    path('shift/list', views.shift_list, name='shift_list'),
    path('test/list', views.test_list, name='test_list'),
    path('color/list', views.color_list, name='color_list'),
    path('color_standard/list', views.color_standard_list, name='color_standard_list'),
]
