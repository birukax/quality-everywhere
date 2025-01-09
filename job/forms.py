from django import forms
from .models import Job
from machine.models import Machine


class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job

        fields = (
            "customer",
            "machine",
            "color_standard",
            "certificate_no",
            "artwork",
        )

    machine = forms.ModelChoiceField(
        queryset=Machine.objects.filter(type="PRESS"),
        required=False,
    )


class CreateFirstOffForm(forms.Form):
    machines = forms.ModelMultipleChoiceField(
        queryset=Machine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
