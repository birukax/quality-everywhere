from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from main.tasks import get_page, role_check
from .models import Product, Artwork
from .tasks import product_get
from .forms import AddArtworkForm, EditArtworkForm
from .filters import ArtworkFilter, ProductFilter


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def list(request):
    products = Product.objects.prefetch_related("jobs", "artworks").all()
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    page = get_page(request, model=products)

    context = {
        "page": page,
        "filter": product_filter,
    }
    return render(request, "product/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def detail(request, id):
    context = {}
    product = Product.objects.get(id=id)
    if Artwork.objects.filter(product=product).exists():
        artwork = Artwork.objects.filter(product=product).latest("created_at")
        context["artwork"] = artwork
    context["product"] = product
    return render(request, "product/detail.html", context)


@login_required
def get(request):
    product_get()
    return redirect("product:list")


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def artwork_list(request):
    artworks = Artwork.objects.all()

    artwork_filter = ArtworkFilter(request.GET, queryset=artworks)
    artworks = artwork_filter.qs
    page = get_page(request, model=artworks)

    context = {
        "page": page,
        "filter": artwork_filter,
    }
    return render(request, "product/artwork/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def artwork_detail(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    context = {"artwork": artwork}
    return render(request, "product/artwork/detail.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
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


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def edit_artwork(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    if request.method == "POST":
        form = EditArtworkForm(request.POST, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect("product:artwork_list")
    else:
        form = EditArtworkForm(instance=artwork)
    context = {"artwork": artwork, "form": form}
    return render(request, "product/artwork/edit.html", context)
