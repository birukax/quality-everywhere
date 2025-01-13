from django import forms
from .models import Job
from machine.models import Machine


class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job

        fields = (
            "customer",
            "press_machine",
            "color_standard",
            "route",
            "artwork_approved",
            "certificate_no",
            "artwork",
        )

    press_machine = forms.ModelChoiceField(
        queryset=Machine.objects.filter(type="PRESS"),
        required=False,
    )


class CreateFirstOffForm(forms.Form):
    machines = forms.ModelMultipleChoiceField(
        queryset=Machine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
