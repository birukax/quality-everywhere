from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.tasks import get_page
from .models import Location, IssueType, Issue, Remark
from .forms import (
    CreateLocationForm,
    CreateIssueTypeForm,
    CreateIssueForm,
    CreateRemarkForm,
)


@login_required
def list(request):
    issues = Issue.objects.all()
    page = get_page(request, model=issues)
    context = {
        "page": page,
    }
    return render(request, "issue/list.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            issue = Issue(
                issue_type=form.cleaned_data["issue_type"],
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


def location_list(request):
    locations = Location.objects.all()
    page = get_page(request, model=locations)
    context = {
        "page": page,
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


def issue_type_list(request):
    issue_types = IssueType.objects.all()
    page = get_page(request, model=issue_types)
    context = {
        "page": page,
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
