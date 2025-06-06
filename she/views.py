from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import formset_factory, modelformset_factory
from main.tasks import get_page, role_check
from .tasks import departments_get, employees_get
from .models import (
    Location,
    IssueType,
    Issue,
    Remark,
    Department,
    IncidentType,
    Incident,
    Employee,
    FPChecklist,
    FirePrevention,
    Checkpoint,
)
from .forms import (
    CreateLocationForm,
    EditLocationForm,
    CreateIssueTypeForm,
    EditIssueTypeForm,
    CreateIssueForm,
    CreateRemarkForm,
    CreateIncidentForm,
    CreateIncidentTypeForm,
    EditIncidentTypeForm,
    CreateCheckpointForm,
    EditCheckpointForm,
    CreateFirePreventionForm,
    FPChecklistForm,
    SubmitFPChecklistForm,
)
from .filters import (
    IssueFilter,
    DepartmentFilter,
    LocationFilter,
    IssueTypeFilter,
    EmployeeFilter,
    IncidentFilter,
    IncidentTypeFilter,
)


@login_required
def issue_list(request):
    user = request.user
    issues = Issue.objects.all()
    # if user.profile.role in ["ADMIN", "MANAGER", "SAFETY"]:
    #     issues = Issue.objects.all()
    # elif user.profile.department:
    #     issues = Issue.objects.filter(
    #         Q(Q(department=user.profile.department) or Q(created_by=user))
    #     )
    # else:
    #     issues = Issue.objects.filter(created_by=user)
    issue_filter = IssueFilter(
        request.GET,
        queryset=issues,
    )
    issues = issue_filter.qs
    page = get_page(request, model=issues)
    context = {
        "page": page,
        "filter": issue_filter,
    }
    return render(request, "issue/list.html", context)


@login_required
def issue_detail(request, id):
    user = request.user
    # if (
    #     user.profile.role not in ["ADMIN", "MANAGER", "SAFETY"]
    #     or user.profile.department
    # ):
    issue = get_object_or_404(Issue, id=id)
    form = CreateRemarkForm()
    context = {
        "issue": issue,
        "form": form,
    }
    return render(request, "issue/detail.html", context)
    # else:
    #     return render(request, "issue/list.html", context)


@login_required
def create_issue(request):
    if request.method == "POST":
        form = CreateIssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user
            issue.save()
            return redirect("she:issue_list")
    else:
        form = CreateIssueForm()

    context = {
        "form": form,
    }
    return render(request, "issue/create.html", context)


@login_required
def update_status(request, id, action):
    issue = get_object_or_404(Issue, id=id)
    if request.method == "POST":
        # if action == "ACCEPT":
        #     action = "ACCEPTED"
        # elif action == "REJECT":
        #     action = "REJECTED"
        # elif action == "COMPLETE":
        #     action = "COMPLETED"
        # elif action == "START":
        #     action = "IN-PROGRESS"
        if action == "APPROVE" and request.user == issue.created_by:
            action = "COMPLETED"
        elif action == "REJECT" and request.user == issue.created_by:
            action = "INCOMPLETE"
        elif action == "CANCEL" and request.user == issue.created_by:
            action = "CANCELLED"
        elif action == "CLOSE":
            action = "PENDING"

        else:
            return
        form = CreateRemarkForm(request.POST)
        if form.is_valid():
            remark = Remark(
                issue=issue,
                action=action,
                text=form.cleaned_data["text"],
            )
            remark.created_by = request.user
            remark.save()
            issue.status = action
            issue.save()
    return redirect("she:issue_detail", id=id)


@login_required
def incident_list(request):
    incidents = Incident.objects.all()
    incident_filter = IncidentFilter(
        request.GET,
        queryset=incidents,
    )
    incidents = incident_filter.qs

    page = get_page(request, model=incidents)
    context = {
        "page": page,
        "filter": incident_filter,
    }
    return render(request, "incident/list.html", context)


@login_required
def incident_detail(request, id):
    incident = get_object_or_404(Incident, id=id)
    context = {
        "incident": incident,
    }
    return render(request, "incident/detail.html", context)


@login_required
def create_incident(request):
    if request.method == "POST":
        form = CreateIncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.created_by = request.user
            incident.save()
            incident.witness_list.set(form.cleaned_data["witness_list"])
            incident.save()
            return redirect("she:incident_list")
    else:
        form = CreateIncidentForm()

    context = {
        "form": form,
    }
    return render(request, "incident/create.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def department_list(request):
    departments = Department.objects.all()
    department_filter = DepartmentFilter(
        request.GET,
        queryset=departments,
    )
    departments = department_filter.qs
    page = get_page(request, model=departments)

    context = {
        "page": page,
        "filter": department_filter,
    }
    return render(request, "issue/department/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def get_departments(request):
    departments_get()
    return redirect("she:department_list")


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def employee_list(request):
    employees = Employee.objects.all()
    employee_filter = EmployeeFilter(
        request.GET,
        queryset=employees,
    )
    employees = employee_filter.qs

    page = get_page(request, model=employees)
    context = {
        "page": page,
        "filter": employee_filter,
    }
    return render(request, "issue/employee/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def get_employees(request):
    employees_get()
    return redirect("she:employee_list")


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def location_list(request):
    locations = Location.objects.all()
    location_filter = LocationFilter(
        request.GET,
        queryset=locations,
    )
    locations = location_filter.qs

    page = get_page(request, model=locations)

    context = {
        "page": page,
        "filter": location_filter,
    }
    return render(request, "issue/location/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def create_location(request):
    if request.method == "POST":
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("she:location_list")
    else:
        form = CreateLocationForm()

    context = {
        "form": form,
    }
    return render(request, "issue/location/create.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def edit_location(request, id):
    location = get_object_or_404(Location, id=id)
    if not location.have_issues:
        if request.method == "POST":
            form = EditLocationForm(request.POST, instance=location)
            if form.is_valid():
                form.save()
                return redirect("she:location_list")
        else:
            form = EditLocationForm(instance=location)

        context = {
            "form": form,
            "location": location,
        }
    return render(request, "issue/location/edit.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def issue_type_list(request):
    issue_types = IssueType.objects.all()
    issue_type_filter = IssueTypeFilter(
        request.GET,
        queryset=issue_types,
    )
    issue_types = issue_type_filter.qs

    page = get_page(request, model=issue_types)
    context = {
        "page": page,
        "filter": issue_type_filter,
    }
    return render(request, "issue/type/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def create_issue_type(request):
    if request.method == "POST":
        form = CreateIssueTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("she:issue_type_list")
    else:
        form = CreateIssueTypeForm()
    context = {"form": form}
    return render(request, "issue/type/create.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def edit_issue_type(request, id):
    issue_type = get_object_or_404(IssueType, id=id)
    if request.method == "POST":
        form = EditIssueTypeForm(request.POST, instance=issue_type)
        if form.is_valid():
            form.save()
            return redirect("she:issue_type_list")
    else:
        form = EditIssueTypeForm(instance=issue_type)
    context = {
        "form": form,
        "issue_type": issue_type,
    }
    return render(request, "issue/type/edit.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def create_incident_type(request):
    if request.method == "POST":
        form = CreateIncidentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("she:incident_type_list")
    else:
        form = CreateIncidentTypeForm()
    return render(request, "incident/type/create.html", {"form": form})


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def edit_incident_type(request, id):
    incident_type = get_object_or_404(IncidentType, id=id)
    if request.method == "POST":
        form = EditIncidentTypeForm(request.POST, instance=incident_type)
        if form.is_valid():
            form.save()
            return redirect("she:incident_type_list")
    else:
        form = EditIncidentTypeForm(instance=incident_type)
    context = {
        "form": form,
        "incident_type": incident_type,
    }
    return render(request, "incident/type/edit.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def incident_type_list(request):
    incident_types = IncidentType.objects.all()
    incident_type_filter = IncidentTypeFilter(
        request.GET,
        queryset=incident_types,
    )
    incident_types = incident_type_filter.qs

    page = get_page(request, model=incident_types)
    context = {
        "page": page,
        "filter": incident_type_filter,
    }
    return render(request, "incident/type/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def checkpoint_list(request):
    checkpoints = Checkpoint.objects.all()

    page = get_page(request, model=checkpoints)

    context = {
        "page": page,
    }
    return render(request, "fire_prevention/checkpoint/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def create_checkpoint(request):
    if request.method == "POST":
        form = CreateCheckpointForm(request.POST)
        if form.is_valid():
            checkpoint = form.save(commit=False)
            checkpoint.created_by = request.user
            checkpoint.save()
            return redirect("she:checkpoint_list")
    else:
        form = CreateCheckpointForm()
    context = {"form": form}
    return render(request, "fire_prevention/checkpoint/create.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def edit_checkpoint(request, id):
    checkpoint = get_object_or_404(Checkpoint, id=id)
    if request.method == "POST":
        form = EditCheckpointForm(request.POST, instance=checkpoint)
        if form.is_valid():
            form.save()
            return redirect("she:checkpoint_list")

    else:
        form = EditCheckpointForm(instance=checkpoint)
    context = {
        "form": form,
        "checkpoint": checkpoint,
    }
    return render(request, "fire_prevention/checkpoint/edit.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def fire_prevention_list(request):
    fire_preventions = FirePrevention.objects.all()

    page = get_page(request, model=fire_preventions)

    context = {
        "page": page,
    }
    return render(request, "fire_prevention/list.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def create_fire_prevention(request):
    if request.method == "POST":
        form = CreateFirePreventionForm(request.POST)
        if form.is_valid():
            fire_prevention = form.save(commit=False)
            fire_prevention.created_by = request.user
            fire_prevention.save()
            checkpoints = Checkpoint.objects.filter(active=True)
            for c in checkpoints:
                FPChecklist.objects.create(
                    fire_prevention=fire_prevention,
                    checkpoint=c,
                )
            return redirect("she:fire_prevention_list")
    else:
        form = CreateFirePreventionForm()

    context = {
        "form": form,
    }
    return render(request, "fire_prevention/create.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def fire_prevention_detail(request, id):
    fire_prevention = get_object_or_404(FirePrevention, id=id)
    can_submit = True
    submit_form = SubmitFPChecklistForm()
    checklists = FPChecklist.objects.filter(fire_prevention=fire_prevention)
    checklist_formset = modelformset_factory(FPChecklist, form=FPChecklistForm, extra=0)
    formset = checklist_formset(queryset=checklists)

    context = {
        "fire_prevention": fire_prevention,
        "checklists": checklists,
        "can_submit": can_submit,
        "submit_form": submit_form,
        "formset": formset,
    }

    return render(request, "fire_prevention/detail.html", context)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def save_fp_checklist(request, id):
    fire_prevention = get_object_or_404(FirePrevention, id=id)
    checklist_formset = modelformset_factory(FPChecklist, form=FPChecklistForm, extra=0)
    formset = checklist_formset(request.POST)
    if formset.is_valid():
        formset.save()
    return redirect("she:fire_prevention_detail", id=id)
