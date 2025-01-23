from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Artwork
from .tasks import product_get
from .forms import AddArtworkForm, EditArtworkForm


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
    context["product"] = product
    return render(request, "product/detail.html", context)


def get(request):
    product_get()
    return redirect("product:list")


def artwork_list(request):
    artworks = Artwork.objects.all()
    context = {"artworks": artworks}
    return render(request, "product/artwork/list.html", context)


def artwork_detail(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    context = {"artwork": artwork}
    return render(request, "product/artwork/detail.html", context)


def add_artwork(request, id):
    context = {}
    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = AddArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = Artwork(
                product=product,
                code=form.cleaned_data["code"],
                approved=form.cleaned_data["approved"],
                remark=form.cleaned_data["remark"],
                file=request.FILES["file"],
                created_by=request.user,
            )
            artwork.save()
            return redirect("product:detail", id=product.id)
    else:
        form = AddArtworkForm()
    context["form"] = form
    context["product"] = product
    return render(request, "product/artwork/add.html", context)


def edit_artwork(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    if request.method == "POST":
        artwork.file = request.FILES["file"]
        artwork.save()
        return redirect("product:detail", id=artwork.product.id)
    context = {"artwork": artwork}
    return render(request, "product/artwork/edit.html", context)
