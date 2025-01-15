from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Test, Conformity, Assessment, FirstOff, OnProcess
from misc.models import ColorStandard, Color
from .tasks import test_create, test_edit, conformity_create, conformity_edit
from .forms import (
    CreateTestForm,
    EditTestForm,
    CreateConformityForm,
    EditConformityForm,
)


@login_required
def list(request, status):
    assessments = Assessment.objects.filter(status=status)
    context = {"assessments": assessments}
    return render(request, "assessment/list.html", context)


@login_required
def detail(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    color_standard = ColorStandard.objects.get(id=assessment.job.color_standard.id)
    tests = FirstOff.objects.filter(assessment=assessment)
    passed = tests.filter(value=True)
    failed = tests.filter(value=False)
    context = {
        "assessment": assessment,
        # "form": assessment_form,
        "color_standard": color_standard,
        # "test_forms": test_forms,
        "tests": tests,
        "passed": passed,
        "failed": failed,
    }
    return render(request, "first_off/detail.html", context)


# @login_required
# def edit(request, id):
#     assessment = get_object_or_404(QualityTest, id=id)
#     form = EditQualityTestForm(instance=assessment)
#     if request.method == "POST":
#         form = EditQualityTestForm(request.POST, instance=assessment)
#         if form.is_valid():
#             form.save()
#             return redirect("assessment:detail", id=assessment.id)
#     context = {"form": form}
#     return render(request, "first_off/edit.html", context)


# @login_required
# def save_tests(request, id):
#     if request.method == "POST":
#         assessment = get_object_or_404(QualityTest, id=id)
#         tests = FirstOff.objects.filter(assessment=assessment)
#         test_forms = [
#             FirstOffTestsFrom(request.POST, instance=instance, prefix=str(instance.id))
#             for instance in tests
#         ]
#         if all([form.is_valid() for form in test_forms]):
#             for form in test_forms:
#                 form.save()
#     return redirect("assessment:detail", id=assessment.id)


@login_required
def test_list(request):
    tests = Test.objects.all()
    context = {"tests": tests}
    return render(request, "assessment/test/list.html", context)


@login_required
def create_test(request):
    if request.method == "GET":
        form = CreateTestForm()
        context = {"form": form}
        return render(request, "assessment/test/create.html", context)

    test_create(request)
    return redirect("assessment:test_list")


@login_required
def edit_test(request, id):
    if request.method == "GET":
        test = get_object_or_404(Test, id=id)
        form = EditTestForm(instance=test)
        context = {"form": form, "test": test}
        return render(request, "assessment/test/edit.html", context)

    test_edit(request, id)
    return redirect("assessment:test_list")


@login_required
def conformity_list(request):
    conformities = Conformity.objects.all()
    context = {"conformities": conformities}
    return render(request, "assessment/conformity/list.html", context)


@login_required
def create_conformity(request):
    if request.method == "GET":
        form = CreateConformityForm()
        context = {"form": form}
        return render(request, "assessment/conformity/create.html", context)

    conformity_create(request)
    return redirect("assessment:conformity_list")


@login_required
def edit_conformity(request, id):
    if request.method == "GET":
        conformity = get_object_or_404(Conformity, id=id)
        form = EditConformityForm(instance=conformity)
        context = {"form": form, "conformity": conformity}
        return render(request, "assessment/conformity/edit.html", context)

    conformity_edit(request, id)
    return redirect("assessment:conformity_list")
