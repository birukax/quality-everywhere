from django import forms
from .models import Machine, Route, MachineRoute
from assesment.models import Test, Conformity


class CreateMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "type", "tests", "conformities")
        widgets = {
            "tests": forms.CheckboxSelectMultiple(),
            "conformities": forms.CheckboxSelectMultiple(),
        }


class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "type", "tests", "conformities")
        widgets = {
            "tests": forms.CheckboxSelectMultiple(),
            "conformities": forms.CheckboxSelectMultiple(),
        }


class CreateRouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("name",)

    machines = forms.IntegerField(min_value=1, max_value=Machine.objects.all().count())


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
