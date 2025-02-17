from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Exists, Q, Count
from main.tasks import get_page
from .tasks import departments_get
from .models import Location, IssueType, Issue, Remark, Department
from .forms import (
    CreateLocationForm,
    CreateIssueTypeForm,
    CreateIssueForm,
    CreateRemarkForm,
)
from .filters import IssueFilter, DepartmentFilter, LocationFilter, IssueTypeFilter


@login_required
def list(request):
    issues = Issue.objects.all()
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
def detail(request, id):
    issue = get_object_or_404(Issue, id=id)
    form = CreateRemarkForm()
    context = {
        "issue": issue,
        "form": form,
    }
    return render(request, "issue/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            issue = Issue(
                issue_type=form.cleaned_data["issue_type"],
                department=form.cleaned_data["department"],
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
            )
            issue.created_by = request.user
            issue.save()
            return redirect("issue:list")
    else:
        form = CreateIssueForm()

    context = {
        "form": form,
    }
    return render(request, "issue/create.html", context)


def update_status(request, id, action):
    issue = get_object_or_404(Issue, id=id)
    if request.method == "POST":
        if action == "ACCEPT":
            action = "ACCEPTED"
        elif action == "APPROVE" and request.user == issue.created_by:
            action = "COMPLETED"
        elif action == "REJECT" and request.user == issue.created_by:
            action = "INCOMPLETE"
        elif action == "REJECT":
            action = "REJECTED"
        elif action == "COMPLETE":
            action = "COMPLETED"
        elif action == "CANCEL":
            action = "CANCELLED"
        # elif action == "START":
        #     action = "IN-PROGRESS"
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
    return redirect("issue:detail", id=id)


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


def get_departments(request):
    departments_get()
    return redirect("issue:department_list")


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


def create_location(request):
    if request.method == "POST":
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("issue:location_list")
    else:
        form = CreateLocationForm()

    context = {
        "form": form,
    }
    return render(request, "issue/location/create.html", context)


def edit_location(request, id):
    pass


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


def create_issue_type(request):
    if request.method == "POST":
        form = CreateIssueTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("issue:issue_type_list")
    else:
        form = CreateIssueTypeForm()
    return render(request, "issue/type/create.html", {"form": form})


def edit_issue_type(request, id):
    pass
