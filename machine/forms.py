from django import forms
from .models import Machine
from assesment.models import Test, Conformity


class CreateMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "tests", "conformities")
        widgets = {
            "tests": forms.CheckboxSelectMultiple(),
            "conformities": forms.CheckboxSelectMultiple(),
        }


class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ("name", "tests", "conformities")
        widgets = {
            "tests": forms.CheckboxSelectMultiple(),
            "conformities": forms.CheckboxSelectMultiple(),
        }
