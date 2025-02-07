from django import forms
from .models import Machine, Route, MachineRoute
from assessment.models import Test, Conformity


class CreateMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "type", "viscosity_test", "tests", "conformities")
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "type": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "viscosity_test": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
            "tests": forms.CheckboxSelectMultiple(
                attrs={"class": "space-y-2  text-blue-600"}
            ),
            "conformities": forms.CheckboxSelectMultiple(
                attrs={"class": "space-y-2 text-sky-600"}
            ),
        }


class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "type", "viscosity_test", "tests", "conformities")
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "type": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "viscosity_test": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
            "tests": forms.CheckboxSelectMultiple(
                attrs={"class": "space-y-2  text-blue-600"}
            ),
            "conformities": forms.CheckboxSelectMultiple(
                attrs={"class": "space-y-2 text-sky-600"}
            ),
        }


class CreateRouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }

    machines = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        machines = cleaned_data.get("machines")
        total_machines = Machine.objects.all().count()
        if machines < 1:
            raise forms.ValidationError("At least one machine is required.")
        if machines > total_machines:
            self.add_error(
                "machines",
                f"The number exceeds the total machines ({total_machines}).",
            )
        return cleaned_data


class EditRouteForm(forms.Form):
    pass


class BaseMachineRouteFormset(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        machines = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                machine = form.cleaned_data["machine"]
                if machine in machines:
                    duplicates = True
                    form.add_error("machine", "Duplicate machines are not allowed.")
                machines.append(machine)
        if duplicates:
            raise forms.ValidationError("Duplicate machines.")
