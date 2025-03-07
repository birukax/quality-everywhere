from django import forms
from django_select2 import forms as s2forms
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
        }

    tests = forms.ModelMultipleChoiceField(
        queryset=Test.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            model=Test,
            max_results=5,
            search_fields=["name__icontains"],
            attrs={"class": "w-full text-center h-auto"},
        ),
    )

    conformities = forms.ModelMultipleChoiceField(
        queryset=Conformity.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            model=Conformity,
            max_results=5,
            search_fields=["name__icontains"],
            attrs={"class": "w-full text-center h-auto"},
        ),
    )


class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("type", "viscosity_test", "tests", "conformities")
        widgets = {
            "type": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "viscosity_test": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }

    tests = forms.ModelMultipleChoiceField(
        queryset=Test.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            Model=Test,
            search_fields=["name__icontains"],
            max_results=5,
            attrs={"class": "w-full text-center h-auto"},
        ),
    )

    conformities = forms.ModelMultipleChoiceField(
        queryset=Conformity.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            model=Conformity,
            search_fields=["name__icontains"],
            max_results=5,
            attrs={"class": "w-full text-center h-auto"},
        ),
    )


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
        if machines == []:
            raise forms.ValidationError("Machine can not be empty.")
