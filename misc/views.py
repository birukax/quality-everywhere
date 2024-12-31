from django.shortcuts import render, redirect, get_object_or_404
from .models import Color, ColorStandard, Machine, Customer, Product, Paper, Shift, Test
from .tasks import get_customer, get_product, create_machine

def machine_list(request):
    machines = Machine.objects.all()
    context = {'machines': machines}
    return render(request, 'misc/machine/list.html', context)

def create_machine(request):
    create_machine(request)
    return redirect('misc:machine_list')

def customer_list(request):
    get_customer()
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'misc/customer/list.html', context)


def product_list(request):
    get_product
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'misc/product/list.html', context)


def paper_list(request):
    papers = Paper.objects.all()
    context = {'papers': papers}
    return render(request, 'misc/paper/list.html', context)


def shift_list(request):
    shifts = Shift.objects.all()
    context = {'shifts': shifts}
    return render(request, 'misc/shift/list.html', context)


def test_list(request):
    tests = Test.objects.all()
    context = {'tests': tests}
    return render(request, 'misc/test/list.html', context)


def color_list(request):
    colors = Color.objects.all()
    context = {'colors': colors}
    return render(request, 'misc/color/list.html', context)


def color_standard_list(request):
    color_standards = ColorStandard.objects.all()
    context = {'color_standards': color_standards}
    return render(request, 'misc/color_standard/list.html', context)