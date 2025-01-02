from django import forms
from .models import Machine


class CreateMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ["name", "tests"]
        widgets = {
            "tests": forms.CheckboxSelectMultiple(),
        }


class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ["tests"]
        widgets = {
            "tests": forms.CheckboxSelectMultiple(),
        }
