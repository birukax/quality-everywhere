from django import forms
from .models import Machine, Route, MachineRoute
from assessment.models import Test, Conformity


class CreateMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "type", "viscosity_test", "tests", "conformities")
        widgets = {
            "name": forms.TextInput(attrs={"style": "width: 10rem"}),
            "viscosity_test": forms.Select(
                attrs={"style": "width: 7rem"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
            "tests": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
            "conformities": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        }


class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "type", "viscosity_test", "tests", "conformities")
        widgets = {
            "name": forms.TextInput(attrs={"style": "width: 10rem"}),
            "viscosity_test": forms.Select(
                attrs={"style": "width: 7rem"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
            "tests": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
            "conformities": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        }


class CreateRouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("name",)

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
