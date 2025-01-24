from django import forms
from .models import Job, JobTest
from machine.models import Machine


class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job

        fields = (
            "customer",
            "color_standard",
            "route",
        )


class CreateJobTestForm(forms.ModelForm):
    class Meta:
        model = JobTest
        fields = ("raw_material", "batch_no")
        widgets = {
            "raw_material": forms.Select(),
            "batch_no": forms.TextInput(attrs={"class": ""}),
        }
