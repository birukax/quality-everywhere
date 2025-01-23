from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Artwork
from .tasks import product_get


def list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product/list.html", context)


def detail(request, id):
    context = {}
    product = Product.objects.get(id=id)
    if Artwork.objects.filter(product=product).exists():
        artwork = Artwork.objects.filter(product=product).latest("created_at")
        context["artwork"] = artwork
        return render(request, "product/detail.html", context)
    context["product"] = product
    return render(request, "product/detail.html", context)


def get(request):
    product_get()
    return redirect("product:list")
