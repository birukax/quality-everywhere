from django.shortcuts import render, get_object_or_404, redirect
from .models import Machine
from .tasks import machine_create, machine_edit
from .forms import CreateMachineForm, EditMachineForm


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
    return redirect("machine:machine_list")


def edit(request, id):
    if request.method == "GET":
        machine = get_object_or_404(Machine, id=id)
        form = EditMachineForm(instance=machine)
        context = {"form": form, "machine": machine}
        return render(request, "machine/edit.html", context)

    machine_edit(request, id)
    return redirect("machine:machine_list")
