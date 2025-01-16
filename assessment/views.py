from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Test, Conformity, Assessment, FirstOff, OnProcess
from misc.models import ColorStandard, Color
from job.models import JobTest
from .tasks import test_create, test_edit, conformity_create, conformity_edit
from django import forms
from .forms import (
    CreateTestForm,
    EditTestForm,
    CreateConformityForm,
    EditConformityForm,
    CreateAssessmentForm,
    EditAssessmentForm,
    FirstOffTestsFrom,
)


@login_required
def list(request, status):
    if status == "OPEN":
        assessments = Assessment.objects.all().exclude(status="COMPLETED")
    else:
        assessments = Assessment.objects.filter(status=status)
    context = {"assessments": assessments}
    return render(request, "first_off/list.html", context)


@login_required
def detail(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    color_standard = ColorStandard.objects.get(id=assessment.job_test.color_standard.id)
    tests = FirstOff.objects.filter(assessment=assessment)
    test_formset = modelformset_factory(FirstOff, form=FirstOffTestsFrom, extra=0)
    edit_assessment_form = EditAssessmentForm(instance=assessment)
    formset = test_formset(queryset=tests)
    passed = tests.filter(value=True)
    failed = tests.filter(value=False)
    context = {
        "assessment": assessment,
        "formset": formset,
        "color_standard": color_standard,
        "edit_assessment_form": edit_assessment_form,
        "tests": tests,
        "passed": passed,
        "failed": failed,
    }
    return render(request, "first_off/detail.html", context)


@login_required
def create_first_off(request, id):
    context = {}
    job_test = JobTest.objects.get(id=id)
    if request.method == "POST":
        form = CreateAssessmentForm(request.POST)
        if form.is_valid():
            machine = job_test.current_machine
            assessment = Assessment(
                job_test=job_test,
                date=form.cleaned_data["date"],
                time=form.cleaned_data["time"],
                shift=form.cleaned_data["shift"],
                machine=machine,
            )
            if machine.tests:
                assessment.save()
                for test in machine.tests.all():
                    first_off = FirstOff(
                        assessment=assessment,
                        test=test,
                    )
                    first_off.save()
                assessment.job_test.status = "FIRST-OFF CREATED"
                assessment.job_test.save()
                return redirect("assessment:detail", id=assessment.id)
    else:
        form = CreateAssessmentForm()
    context["form"] = form
    context["job_test"] = job_test
    return render(request, "first_off/create.html", context)


@login_required
def create_on_process(request, id):
    context = {}
    job_test = JobTest.objects.get(id=id)
    if request.method == "POST":
        form = CreateAssessmentForm(request.POST)
        if form.is_valid():
            machine = job_test.current_machine
            assessment = Assessment(
                job_test=job_test,
                date=form.cleaned_data["date"],
                time=form.cleaned_data["time"],
                shift=form.cleaned_data["shift"],
                machine=machine,
            )
            if machine.tests:
                assessment.save()
                assessment.job_test.status = "ON PROCESS CREATED"
                assessment.job_test.save()
                return redirect("assessment:detail", id=assessment.id)
    else:
        form = CreateAssessmentForm()
    context["form"] = form
    context["job_test"] = job_test
    return render(request, "on_process/create.html", context)


@login_required
def edit(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    form = EditAssessmentForm(instance=assessment)
    if request.method == "POST":
        form = EditAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            return redirect("assessment:detail", id=assessment.id)
    context = {"form": form}
    return render(request, "first_off/edit.html", context)


@login_required
def save_tests(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    test_formset = modelformset_factory(FirstOff, form=FirstOffTestsFrom, extra=0)
    formset = test_formset(request.POST)
    if formset.is_valid():
        formset.save()
    return redirect("assessment:detail", id=assessment.id)


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
