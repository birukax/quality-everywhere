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
        widgets = {
            "customer": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "color_standard": forms.Select(
                attrs={"class": "w-full text-center h-auto"}
            ),
            "route": forms.Select(attrs={"class": "w-full text-center h-auto"}),
        }


class CreateJobTestForm(forms.ModelForm):
    class Meta:
        model = JobTest
        fields = ("raw_material", "batch_no")
        widgets = {
            "raw_material": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "batch_no": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }
