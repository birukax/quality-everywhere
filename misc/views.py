from django.shortcuts import render, redirect, get_object_or_404
from .models import Color, ColorStandard, Customer, RawMaterial, Shift
from main.tasks import get_page
from .tasks import (
    customer_get,
    raw_material_create,
    raw_material_edit,
    shift_create,
    shift_edit,
    color_create,
    color_edit,
    color_standard_create,
    color_standard_edit,
)
from .filters import (
    CustomerFilter,
    ColorFilter,
    ColorStandardFilter,
    RawMaterialFilter,
    ShiftFilter,
)
from .forms import (
    CreateRawMaterialForm,
    EditRawMaterialForm,
    CreateShiftForm,
    EditShiftForm,
    CreateColorForm,
    EditColorForm,
    CreateColorStandardForm,
    EditColorStandardForm,
)


def customer_list(request):
    customers = Customer.objects.all()
    customer_filter = CustomerFilter(request.GET, queryset=customers)
    customers = customer_filter.qs
    page = get_page(request, model=customers)

    context = {
        "page": page,
        "filter": customer_filter,
    }
    return render(request, "misc/customer/list.html", context)


def get_customers(request):
    customer_get()
    return redirect("misc:customer_list")


def raw_material_list(request):
    raw_materials = RawMaterial.objects.all()
    raw_material_filter = RawMaterialFilter(request.GET, queryset=raw_materials)
    raw_materials = raw_material_filter.qs
    page = get_page(request, model=raw_materials)
    context = {
        "page": page,
        "filter": raw_material_filter,
    }
    return render(request, "misc/raw_material/list.html", context)


def create_raw_material(request):
    if request.method == "GET":
        form = CreateRawMaterialForm()
        context = {"form": form}
        return render(request, "misc/raw_material/create.html", context)

    raw_material_create(request)
    return redirect("misc:raw_material_list")


def edit_raw_material(request, id):
    if request.method == "GET":
        raw_material = get_object_or_404(RawMaterial, id=id)
        form = EditRawMaterialForm(instance=raw_material)
        context = {"form": form, "raw_material": raw_material}
        return render(request, "misc/raw_material/edit.html", context)

    raw_material_edit(request, id)
    return redirect("misc:raw_material_list")


def shift_list(request):
    shifts = Shift.objects.all()
    shift_filter = ShiftFilter(request.GET, queryset=shifts)
    shifts = shift_filter.qs
    page = get_page(request, model=shifts)
    context = {
        "page": page,
        "filter": shift_filter,
    }
    return render(request, "misc/shift/list.html", context)


def create_shift(request):
    if request.method == "GET":
        form = CreateShiftForm()
        context = {"form": form}
        return render(request, "misc/shift/create.html", context)

    shift_create(request)
    return redirect("misc:shift_list")


def edit_shift(request, id):
    if request.method == "GET":
        shift = get_object_or_404(Shift, id=id)
        form = EditShiftForm(instance=shift)
        context = {"form": form, "shift": shift}
        return render(request, "misc/shift/edit.html", context)

    shift_edit(request, id)
    return redirect("misc:shift_list")


def color_list(request):
    colors = Color.objects.all()
    color_filter = ColorFilter(request.GET, queryset=colors)
    colors = color_filter.qs
    page = get_page(request, model=colors)
    context = {
        "page": page,
        "filter": color_filter,
    }
    return render(request, "misc/color/list.html", context)


def create_color(request):
    if request.method == "GET":
        form = CreateColorForm()
        context = {"form": form}
        return render(request, "misc/color/create.html", context)

    color_create(request)
    return redirect("misc:color_list")


def edit_color(request, id):
    if request.method == "GET":
        color = get_object_or_404(Color, id=id)
        form = EditColorForm(instance=color)
        context = {"form": form, "color": color}
        return render(request, "misc/color/edit.html", context)

    color_edit(request, id)
    return redirect("misc:color_list")


def color_standard_list(request):
    color_standards = ColorStandard.objects.all()
    color_standard_filter = ColorStandardFilter(request.GET, queryset=color_standards)
    color_standards = color_standard_filter.qs
    page = get_page(request, model=color_standards)
    context = {
        "page": page,
        "filter": color_standard_filter,
    }
    return render(request, "misc/color_standard/list.html", context)


def create_color_standard(request):
    if request.method == "GET":
        form = CreateColorStandardForm()
        context = {"form": form}
        return render(request, "misc/color_standard/create.html", context)

    color_standard_create(request)
    return redirect("misc:color_standard_list")


def edit_color_standard(request, id):
    if request.method == "GET":
        color_standard = get_object_or_404(ColorStandard, id=id)
        form = EditColorStandardForm(instance=color_standard)
        context = {"form": form, "color_standard": color_standard}
        return render(request, "misc/color_standard/edit.html", context)

    color_standard_edit(request, id)
    return redirect("misc:color_standard_list")
