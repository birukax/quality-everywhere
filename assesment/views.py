from django.shortcuts import render, redirect, get_object_or_404
from .models import Test
from .tasks import test_create, test_edit
from .forms import CreateTestForm, EditTestForm


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
    return redirect("misc:test_list")


def edit_test(request, id):
    if request.method == "GET":
        test = get_object_or_404(Test, id=id)
        form = EditTestForm(instance=test)
        context = {"form": form, "test": test}
        return render(request, "misc/test/edit.html", context)

    test_edit(request, id)
    return redirect("misc:test_list")
