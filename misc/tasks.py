import pyodbc
import requests
from .models import Product, Customer, Paper, Shift, Test, Color, ColorStandard
from decouple import config
from requests_ntlm import HttpNtlmAuth
from django.shortcuts import get_object_or_404
from .forms import (
    CreatePaperForm,
    EditPaperForm,
    CreateShiftForm,
    EditShiftForm,
    CreateTestForm,
    EditTestForm,
    CreateColorForm,
    EditColorForm,
    CreateColorStandardForm,
    EditColorStandardForm,
)


def product_get():
    url = config("NAV_FINISHED_ITEMS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for product in data["value"]:
                product = Product(
                    no=product["No"],
                    name=product["Description"],
                )
                if Product.objects.filter(no=product.no).exists():
                    pass
                else:
                    product.save()
    except Exception as e:
        print(e)


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


def paper_create(request):
    if request.method == "POST":
        form = CreatePaperForm(request.POST)
        if form.is_valid():
            form.save()


def paper_edit(request, id):
    paper = get_object_or_404(Paper, id=id)
    if request.method == "POST":
        form = EditPaperForm(request.POST, instance=paper)
        if form.is_valid():
            paper.name = form.cleaned_data["name"]
            paper.no = form.cleaned_data["no"]
            paper.save()


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


def test_create(request):
    if request.method == "POST":
        form = CreateTestForm(request.POST)
        if form.is_valid():
            form.save()


def test_edit(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == "POST":
        form = EditTestForm(request.POST, instance=test)
        if form.is_valid():
            test.name = form.cleaned_data["name"]
            test.save()


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
            color.color_standard = form.cleaned_data["color_standard"]
            color.save()


def color_standard_create(request):
    if request.method == "POST":
        form = CreateColorStandardForm(request.POST)
        if form.is_valid():
            form.save()


def color_standard_edit(request, id):
    color_standard = get_object_or_404(ColorStandard, id=id)
    if request.method == "POST":
        form = EditColorStandardForm(request.POST, instance=color_standard)
        if form.is_valid():
            color_standard.name = form.cleaned_data["name"]
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
