from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FirstOff
from assesment.models import FirstOffTest
from misc.models import ColorStandard
from .forms import EditFirstOffForm, FirstOffTestsFrom


@login_required
def list(request, status):
    first_offs = FirstOff.objects.filter(status=status)
    context = {"first_offs": first_offs}
    return render(request, "first_off/list.html", context)


@login_required
def detail(request, id):
    first_off = get_object_or_404(FirstOff, id=id)
    edit_first_off_form = EditFirstOffForm(instance=first_off)
    color_standard = ColorStandard.objects.get(id=first_off.job.color_standard.id)
    tests = FirstOffTest.objects.filter(first_off=first_off)
    passed = tests.filter(value=True)
    failed = tests.filter(value=False)
    test_forms = [
        FirstOffTestsFrom(instance=instance, prefix=str(instance.id))
        for instance in tests
    ]
    context = {
        "first_off": first_off,
        "edit_first_off_form": edit_first_off_form,
        "color_standard": color_standard,
        "test_forms": test_forms,
        "tests": tests,
        "passed": passed,
        "failed": failed,
    }
    return render(request, "first_off/detail.html", context)


@login_required
def edit(request, id):
    first_off = get_object_or_404(FirstOff, id=id)
    form = EditFirstOffForm(instance=first_off)
    if request.method == "POST":
        form = EditFirstOffForm(request.POST, instance=first_off)
        if form.is_valid():
            form.save()
            return redirect("first_off:detail", id=first_off.id)
    context = {"form": form}
    return render(request, "first_off/edit.html", context)


@login_required
def save_tests(request, id):
    if request.method == "POST":
        first_off = get_object_or_404(FirstOff, id=id)
        tests = FirstOffTest.objects.filter(first_off=first_off)
        test_forms = [
            FirstOffTestsFrom(request.POST, instance=instance, prefix=str(instance.id))
            for instance in tests
        ]
        if all([form.is_valid() for form in test_forms]):
            for form in test_forms:
                form.save()
    return redirect("first_off:detail", id=first_off.id)
