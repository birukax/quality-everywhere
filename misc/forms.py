from django import forms
from .models import Machine, Paper, Shift


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


class CreatePaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ["no", "name"]


class EditPaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ["no", "name"]


class CreateShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["code", "name"]


class EditShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["code", "name"]
