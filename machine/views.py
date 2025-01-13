from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Machine, Route, MachineRoute
from .tasks import machine_create, machine_edit
from .forms import (
    CreateMachineForm,
    EditMachineForm,
    CreateRouteForm,
    EditRouteForm,
    BaseMachineRouteFormset,
)


def list(request):
    machines = Machine.objects.all()
    context = {"machines": machines}
    return render(request, "machine/list.html", context)


def create(request):
    if request.method == "GET":
        form = CreateMachineForm()
        context = {"form": form}
        return render(request, "machine/create.html", context)

    machine_create(request)
    return redirect("machine:list")


def edit(request, id):
    if request.method == "GET":
        machine = get_object_or_404(Machine, id=id)
        form = EditMachineForm(instance=machine)
        context = {"form": form, "machine": machine}
        return render(request, "machine/edit.html", context)

    machine_edit(request, id)
    return redirect("machine:list")


def route_list(request):
    routes = Route.objects.all()
    create_route_form = CreateRouteForm()
    context = {"routes": routes, "create_route_form": create_route_form}
    return render(request, "machine/route/list.html", context)


def create_route(request):
    if request.method == "POST":
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            route = Route(
                name=form.cleaned_data["name"],
            )
            route.save()
            machines = form.cleaned_data["machines"]
            for m in range(1, machines + 1):
                print(m)
                machine_route = MachineRoute(
                    route=route,
                    order=m,
                )
                machine_route.save()
            return redirect("machine:update_machine_route", id=route.id)
        else:
            return redirect("machine:route_list")


def edit_route(request):
    pass


def update_machine_route(request, id):
    context = {}
    route = get_object_or_404(Route, id=id)
    route_formset = modelformset_factory(
        MachineRoute,
        fields=("machine",),
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


def cancel_create_route(request, id):
    route = get_object_or_404(Route, id=id)
    route.delete()
    return redirect("machine:route_list")
