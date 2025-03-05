from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from main.tasks import get_page, role_check
from .models import Machine, Route, MachineRoute
from .filters import MachineFilter, RouteFilter
from .forms import (
    CreateMachineForm,
    EditMachineForm,
    CreateRouteForm,
    EditRouteForm,
    BaseMachineRouteFormset,
)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def list(request):
    machines = Machine.objects.prefetch_related("tests", "conformities").all()
    machine_filter = MachineFilter(
        request.GET,
        queryset=machines,
    )
    machines = machine_filter.qs
    page = get_page(request, model=machines)

    context = {
        "page": page,
        "filter": machine_filter,
    }
    return render(request, "machine/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def create(request):
    context = {}
    if request.method == "POST":
        form = CreateMachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("machine:list")
    else:
        form = CreateMachineForm()
    context = {"form": form}
    return render(request, "machine/create.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def edit(request, id):
    machine = get_object_or_404(Machine, id=id)
    if request.method == "POST":
        form = EditMachineForm(request.POST, instance=machine)
        if form.is_valid():
            tests = form.cleaned_data["tests"]
            conformities = form.cleaned_data["conformities"]
            machine.type = form.cleaned_data["type"]
            machine.tests.set(tests)
            machine.conformities.set(conformities)
            machine.save()
            return redirect("machine:list")
    else:
        form = EditMachineForm(instance=machine)
    context = {"form": form, "machine": machine}
    return render(request, "machine/edit.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def route_list(request):
    routes = Route.objects.prefetch_related("route_machines").all()
    route_filter = RouteFilter(
        request.GET,
        queryset=routes,
    )
    routes = route_filter.qs
    page = get_page(request, model=routes)

    create_route_form = CreateRouteForm()
    context = {
        "page": page,
        "filter": route_filter,
        "create_route_form": create_route_form,
    }
    return render(request, "machine/route/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def create_route(request):
    context = {}
    if request.method == "POST":
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            route = Route(
                name=form.cleaned_data["name"],
            )
            route.save()
            machines = form.cleaned_data["machines"]
            for m in range(1, machines + 1):
                machine_route = MachineRoute(
                    route=route,
                    order=m,
                )
                machine_route.save()
            return redirect("machine:update_machine_route", id=route.id)
    else:
        form = CreateRouteForm()
    context["create_route_form"] = form
    return render(request, "machine/route/list.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def edit_route(request):
    pass


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def update_machine_route(request, id):
    context = {}
    route = get_object_or_404(Route, id=id)
    route_formset = modelformset_factory(
        MachineRoute,
        fields=("machine",),
        widgets={
            "machine": forms.Select(attrs={"class": "w-full text-center h-auto"}),
        },
        formset=BaseMachineRouteFormset,
        extra=0,
    )
    context["route"] = route
    if request.method == "POST":
        formset = route_formset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("machine:route_list")
    else:
        formset = route_formset(queryset=MachineRoute.objects.filter(route=route))
    context["formset"] = formset
    return render(request, "machine/route/update.html", context)


@login_required
@role_check(["ADMIN", "MANAGER", "INSPECTOR", "SUPERVISOR"])
def cancel_create_route(request, id):
    route = get_object_or_404(Route, id=id)
    route.delete()
    return redirect("machine:route_list")
