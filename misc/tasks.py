import requests
from django.shortcuts import redirect
from .models import Customer, RawMaterial, Shift, Color, ColorStandard
from decouple import config
from requests_ntlm import HttpNtlmAuth
from django.shortcuts import get_object_or_404
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


def customer_get():
    url = config("NAV_CUSTOMERS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for customer in data["value"]:
                customer = Customer(
                    no=customer["No"],
                    name=customer["Name"],
                )
                if Customer.objects.filter(no=customer.no).exists():
                    pass
                else:
                    customer.save()
    except Exception as e:
        print(e)


def raw_material_create(request):
    if request.method == "POST":
        form = CreateRawMaterialForm(request.POST)
        if form.is_valid():
            form.save()


def raw_material_edit(request, id):
    raw_material = get_object_or_404(RawMaterial, id=id)
    if request.method == "POST":
        form = EditRawMaterialForm(request.POST, instance=raw_material)
        if form.is_valid():
            raw_material.name = form.cleaned_data["name"]
            raw_material.no = form.cleaned_data["no"]
            raw_material.save()


def shift_create(request):
    if request.method == "POST":
        form = CreateShiftForm(request.POST)
        if form.is_valid():
            form.save()


def shift_edit(request, id):
    shift = get_object_or_404(Shift, id=id)
    if request.method == "POST":
        form = EditShiftForm(request.POST, instance=shift)
        if form.is_valid():
            shift.name = form.cleaned_data["name"]
            shift.code = form.cleaned_data["code"]
            shift.save()


def color_create(request):
    if request.method == "POST":
        form = CreateColorForm(request.POST)
        if form.is_valid():
            form.save()


def color_edit(request, id):
    color = get_object_or_404(Color, id=id)
    if request.method == "POST":
        form = EditColorForm(request.POST, instance=color)
        if form.is_valid():
            color.name = form.cleaned_data["name"]
            color.code = form.cleaned_data["code"]
            color.viscosity = form.cleaned_data["viscosity"]
            color.save()


def color_standard_edit(request, id):
    color_standard = get_object_or_404(ColorStandard, id=id)
    if request.method == "POST":
        form = EditColorStandardForm(request.POST, instance=color_standard)
        if form.is_valid():
            color_standard.name = form.cleaned_data["name"]
            color_standard.colors.set(form.cleaned_data["colors"])
            color_standard.save()


# def get_machine():
#     url = config("NAV_MACHINES")
#     user = config("NAV_INSTANCE_USER")
#     password = config("NAV_INSTANCE_PASSWORD")
#     auth = HttpNtlmAuth(user, password)
#     try:
#         response = requests.get(url, auth=auth)
#         if response.ok:
#             data = response.json()
#             for machine in data["value"]:
#                 machine = Machine(
#                     code=machine["No"],
#                     name=machine["Name"],
#                     type=machine["Work_Center_No"],
#                 )
#                 if Machine.objects.filter(code=machine.code).exists():
#                     pass
#                 else:
#                     machine.save()
#     except Exception as e:
#         print(e)
