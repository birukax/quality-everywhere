from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Conformity
from .tasks import test_create, test_edit, conformity_create, conformity_edit
from .forms import (
    CreateTestForm,
    EditTestForm,
    CreateConformityForm,
    EditConformityForm,
)


def test_list(request):
    tests = Test.objects.all()
    context = {"tests": tests}
    return render(request, "misc/test/list.html", context)


def create_test(request):
    if request.method == "GET":
        form = CreateTestForm()
        context = {"form": form}
        return render(request, "misc/test/create.html", context)

    test_create(request)
    return redirect("assesment:test_list")


def edit_test(request, id):
    if request.method == "GET":
        test = get_object_or_404(Test, id=id)
        form = EditTestForm(instance=test)
        context = {"form": form, "test": test}
        return render(request, "misc/test/edit.html", context)

    test_edit(request, id)
    return redirect("assesment:test_list")


def conformity_list(request):
    conformities = Conformity.objects.all()
    context = {"conformities": conformities}
    return render(request, "misc/conformity/list.html", context)


def create_conformity(request):
    if request.method == "GET":
        form = CreateConformityForm()
        context = {"form": form}
        return render(request, "misc/conformity/create.html", context)

    conformity_create(request)
    return redirect("assesment:conformity_list")


def edit_conformity(request, id):
    if request.method == "GET":
        conformity = get_object_or_404(Conformity, id=id)
        form = EditConformityForm(instance=conformity)
        context = {"form": form, "conformity": conformity}
        return render(request, "misc/conformity/edit.html", context)

    conformity_edit(request, id)
    return redirect("assesment:conformity_list")
