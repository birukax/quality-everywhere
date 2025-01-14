from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import QualityTest
from assesment.models import FirstOff
from misc.models import ColorStandard
from .forms import EditQualityTestForm, FirstOffTestsFrom


@login_required
def list(request, status):
    quality_tests = QualityTest.objects.filter(status=status)
    context = {"quality_tests": quality_tests}
    return render(request, "first_off/list.html", context)


@login_required
def detail(request, id):
    quality_test = get_object_or_404(QualityTest, id=id)
    edit_quality_test_form = EditQualityTestForm(instance=quality_test)
    color_standard = ColorStandard.objects.get(id=quality_test.job.color_standard.id)
    tests = FirstOff.objects.filter(quality_test=quality_test)
    passed = tests.filter(value=True)
    failed = tests.filter(value=False)
    test_forms = [
        FirstOffTestsFrom(instance=instance, prefix=str(instance.id))
        for instance in tests
    ]
    context = {
        "quality_test": quality_test,
        "edit_quality_test_form": edit_quality_test_form,
        "color_standard": color_standard,
        "test_forms": test_forms,
        "tests": tests,
        "passed": passed,
        "failed": failed,
    }
    return render(request, "first_off/detail.html", context)


@login_required
def edit(request, id):
    quality_test = get_object_or_404(QualityTest, id=id)
    form = EditQualityTestForm(instance=quality_test)
    if request.method == "POST":
        form = EditQualityTestForm(request.POST, instance=quality_test)
        if form.is_valid():
            form.save()
            return redirect("quality_test:detail", id=quality_test.id)
    context = {"form": form}
    return render(request, "first_off/edit.html", context)


@login_required
def save_tests(request, id):
    if request.method == "POST":
        quality_test = get_object_or_404(QualityTest, id=id)
        tests = FirstOff.objects.filter(quality_test=quality_test)
        test_forms = [
            FirstOffTestsFrom(request.POST, instance=instance, prefix=str(instance.id))
            for instance in tests
        ]
        if all([form.is_valid() for form in test_forms]):
            for form in test_forms:
                form.save()
    return redirect("quality_test:detail", id=quality_test.id)
