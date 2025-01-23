from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .tasks import product_get


def list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product/list.html", context)


def get(request):
    product_get()
    return redirect("product:list")
