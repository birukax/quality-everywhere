from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, formset_factory
from django.db.models import Sum
from misc.models import ColorStandard, Color
from job.models import JobTest
from approval.models import AssessmentApproval
from main.tasks import get_page
from .tasks import test_create, test_edit, conformity_create, conformity_edit
from .models import (
    Test,
    Conformity,
    Assessment,
    FirstOff,
    OnProcess,
    Waste,
    SemiWaste,
    Viscosity,
    Lamination,
    Substrate,
)
from .filters import (
    AssessmentFilter,
    SemiWasteFilter,
    WasteFilter,
    ConformityFilter,
    TestFilter,
)
from .forms import (
    CreateTestForm,
    EditTestForm,
    CreateConformityForm,
    EditConformityForm,
    CreateAssessmentForm,
    EditAssessmentForm,
    FirstOffTestsFrom,
    OnProcessConformitiesForm,
    CreateWasteForm,
    SampleForm,
    CreateViscosityForm,
    UpdateSemiWasteForm,
    CreateLaminationForm,
    LaminationSubstratesForm,
)


@login_required
def first_off_list(request, status):
    if status == "OPEN":
        assessments = Assessment.objects.filter(type="FIRST-OFF").exclude(
            status="COMPLETED"
        )
    else:
        assessments = Assessment.objects.filter(type="FIRST-OFF", status=status)
    assessment_filter = AssessmentFilter(request.GET, queryset=assessments)
    assessments = assessment_filter.qs
    page = get_page(request, model=assessments)

    context = {
        "page": page,
        "filter": assessment_filter,
    }
    return render(request, "first_off/list.html", context)


@login_required
def on_process_list(request, status):
    if status == "OPEN":
        assessments = Assessment.objects.filter(type="ON-PROCESS").exclude(
            status="COMPLETED"
        )
    else:
        assessments = Assessment.objects.filter(type="ON-PROCESS", status=status)
    assessment_filter = AssessmentFilter(request.GET, queryset=assessments)
    assessments = assessment_filter.qs
    page = get_page(request, model=assessments)

    context = {
        "page": page,
        "filter": assessment_filter,
    }
    return render(request, "on_process/list.html", context)


@login_required
def first_off_detail(request, id):
    can_submit = True
    assessment = get_object_or_404(Assessment, id=id)
    approvals = AssessmentApproval.objects.filter(assessment=assessment)
    color_standard = ColorStandard.objects.get(id=assessment.job_test.color_standard.id)
    tests = FirstOff.objects.filter(assessment=assessment)
    test_formset = modelformset_factory(FirstOff, form=FirstOffTestsFrom, extra=0)
    edit_assessment_form = EditAssessmentForm(instance=assessment)
    formset = test_formset(queryset=tests)
    passed = tests.filter(value=True)
    failed = tests.filter(value=False)
    if passed.count() == 0 and failed.count() == 0:
        can_submit = False
    context = {
        "assessment": assessment,
        "approvals": approvals,
        "formset": formset,
        "color_standard": color_standard,
        "edit_assessment_form": edit_assessment_form,
        "tests": tests,
        "passed": passed,
        "failed": failed,
        "can_submit": can_submit,
    }

    return render(request, "first_off/detail.html", context)


@login_required
def on_process_detail(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    edit_assessment_form = EditAssessmentForm(instance=assessment)
    color_standard = ColorStandard.objects.get(id=assessment.job_test.color_standard.id)
    lamination = Lamination.objects.filter(assessment=assessment).first()
    colors = [
        {
            "color_id": color.id,
            "color_name": color.name,
            "color_viscosity": color.viscosity,
        }
        for color in color_standard.colors.all()
    ]
    conformities = OnProcess.objects.filter(assessment=assessment)
    conformity_form = OnProcessConformitiesForm()
    wastes = Waste.objects.filter(assessment=assessment)
    conformity_form.fields["conformity"].queryset = assessment.machine.conformities
    total_waste = wastes.aggregate(total=Sum("quantity"))["total"] or 0
    create_waste_form = CreateWasteForm()
    viscosities = Viscosity.objects.filter(assessment=assessment)
    sample_form = SampleForm()
    viscosities_formset = formset_factory(form=CreateViscosityForm, extra=0)
    formset = viscosities_formset(initial=colors)
    lamination_substrates_formset = modelformset_factory(
        Substrate, form=LaminationSubstratesForm, extra=0
    )
    substrates_formset = lamination_substrates_formset(
        queryset=Substrate.objects.filter(lamination=lamination)
    )
    context = {
        "assessment": assessment,
        "lamination": lamination,
        "substrates_formset": substrates_formset,
        "color_standard": color_standard,
        "edit_assessment_form": edit_assessment_form,
        "create_waste_form": create_waste_form,
        "conformities": conformities,
        "wastes": wastes,
        "viscosities": viscosities,
        "total_waste": total_waste,
        "form": conformity_form,
        "sample_form": sample_form,
        "formset": formset,
    }
    return render(request, "on_process/detail.html", context)


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
                type="FIRST-OFF",
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
                return redirect("assessment:first_off_detail", id=assessment.id)
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
        lamination_form = CreateLaminationForm(request.POST)
        if form.is_valid() and lamination_form.is_valid():
            machine = job_test.current_machine
            assessment = Assessment(
                job_test=job_test,
                shift=form.cleaned_data["shift"],
                machine=machine,
                type="ON-PROCESS",
            )

            if machine.tests:
                assessment.save()
                lamination = lamination_form.save(commit=False)
                lamination.assessment = assessment
                lamination.save()
                ply_structure = lamination_form.cleaned_data["ply_structure"]
                for p in range(0, ply_structure):
                    substrate = Substrate(lamination=lamination)
                    substrate.save()
                assessment.job_test.status = "ON-PROCESS CREATED"
                assessment.job_test.save()
                return redirect("assessment:on_process_detail", id=assessment.id)
    else:
        form = CreateAssessmentForm()
        lamination_form = CreateLaminationForm()

    context["form"] = form
    context["lamination_form"] = lamination_form
    context["job_test"] = job_test
    return render(request, "on_process/create.html", context)


@login_required
def edit_first_off(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    form = EditAssessmentForm(instance=assessment)
    if request.method == "POST":
        form = EditAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
    return redirect("assessment:first_off_detail", id=assessment.id)


@login_required
def edit_on_process(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    form = EditAssessmentForm(instance=assessment)
    if request.method == "POST":
        form = EditAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
    return redirect("assessment:on_process_detail", id=assessment.id)


@login_required
def save_test(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    test_formset = modelformset_factory(FirstOff, form=FirstOffTestsFrom, extra=0)
    formset = test_formset(request.POST)
    if formset.is_valid():
        formset.save()
    return redirect("assessment:first_off_detail", id=assessment.id)


@login_required
def save_conformity(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    conformity_form = OnProcessConformitiesForm(request.POST)
    if conformity_form.is_valid():
        conformity = conformity_form.save(commit=False)
        conformity.assessment = assessment
        conformity.created_by = request.user
        conformity.shift = assessment.shift
        conformity.save()
    return redirect("assessment:on_process_detail", id=assessment.id)


@login_required
def save_viscosity(request, id):
    assessment = Assessment.objects.get(id=id)
    if request.method == "POST":
        viscosities_formset = formset_factory(form=CreateViscosityForm, extra=0)
        sample_form = SampleForm(request.POST)
        formset = viscosities_formset(request.POST)
        if sample_form.is_valid() and formset.is_valid():
            sample_no = sample_form.cleaned_data["sample_no"]
            for form in formset:
                if form.cleaned_data:
                    color = Color.objects.get(id=form.cleaned_data["color_id"])
                    viscosity = Viscosity(
                        sample_no=sample_no,
                        assessment=assessment,
                        color=color,
                        value=form.cleaned_data["value"],
                        created_by=request.user,
                    )
                    viscosity.save()
        else:
            print(formset.errors)
    return redirect("assessment:on_process_detail", id=assessment.id)


@login_required
def update_substrates(request, id):
    assessment = Assessment.objects.get(id=id)
    if request.method == "POST":
        substrates_formset = modelformset_factory(
            Substrate, form=LaminationSubstratesForm, extra=0
        )
        formset = substrates_formset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
    return redirect("assessment:on_process_detail", id=assessment.id)


@login_required
def create_waste(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    if request.method == "POST":
        form = CreateWasteForm(request.POST)
        if form.is_valid():
            waste = form.save(commit=False)
            waste.assessment = assessment
            waste.machine = assessment.machine
            waste.shift = assessment.shift
            waste.save()
    return redirect("assessment:on_process_detail", id=assessment.id)


@login_required
def test_list(request):
    tests = Test.objects.all()
    test_filter = TestFilter(
        request.GET,
        queryset=tests,
    )
    tests = test_filter.qs
    page = get_page(request, model=tests)

    context = {
        "page": page,
        "filter": test_filter,
    }
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
    conformity_filter = ConformityFilter(request.GET, queryset=conformities)
    conformities = conformity_filter.qs
    page = get_page(request, model=conformities)

    context = {
        "page": page,
        "filter": conformity_filter,
    }
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


@login_required
def waste_list(request):
    wastes = Waste.objects.all()
    waste_filter = WasteFilter(
        request.GET,
        queryset=wastes,
    )
    wastes = waste_filter.qs
    page = get_page(request, model=wastes)
    context = {
        "page": page,
        "filter": waste_filter,
    }
    return render(request, "assessment/waste/list.html", context)


@login_required
def semi_waste_list(request):
    semi_wastes = SemiWaste.objects.all()
    semi_waste_filter = SemiWasteFilter(
        request.GET,
        queryset=semi_wastes,
    )
    semi_wastes = semi_waste_filter.qs
    page = get_page(request, model=semi_wastes)

    context = {
        "page": page,
        "filter": semi_waste_filter,
    }
    return render(request, "assessment/semi_waste/list.html", context)


@login_required
def update_semi_waste(request, id):
    context = {}
    semi_waste = get_object_or_404(SemiWaste, id=id)
    if request.method == "POST":
        form = UpdateSemiWasteForm(request.POST, instance=semi_waste)
        if form.is_valid():
            semi_waste.approved_by = request.user
            semi_waste.approved_quantity = form.cleaned_data["approved_quantity"]
            semi_waste.rejected_quantity = (
                semi_waste.quantity - form.cleaned_data["approved_quantity"]
            )
            semi_waste.status = "COMPLETED"
            semi_waste.save()
            return redirect("assessment:semi_waste_list")
    else:
        form = UpdateSemiWasteForm(instance=semi_waste)
    context["form"] = form
    context["semi_waste"] = semi_waste
    return render(
        request,
        "assessment/semi_waste/update.html",
        context,
    )
