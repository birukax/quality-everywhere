from django.shortcuts import get_object_or_404
from .models import Machine
from .forms import CreateMachineForm, EditMachineForm


def machine_create(request):
    if request.method == "POST":
        form = CreateMachineForm(request.POST)
        if form.is_valid():
            form.save()


def machine_edit(request, id):
    machine = get_object_or_404(Machine, id=id)
    if request.method == "POST":
        form = EditMachineForm(request.POST, instance=machine)
        if form.is_valid():
            tests = form.cleaned_data["tests"]
            conformities = form.cleaned_data["conformities"]
            machine.tests.set(tests)
            machine.conformities.set(conformities)
            machine.save()
