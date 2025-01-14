from django import forms
from .models import Job, JobTest
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


class CreateJobTestForm(forms.ModelForm):
    class Meta:
        model = JobTest
        fields = ("paper", "batch_no")
        widgets = {
            "paper": forms.Select(),
            "batch_no": forms.TextInput(attrs={"class": ""}),
        }
