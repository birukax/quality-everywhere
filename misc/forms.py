from django import forms
from .models import Machine, Paper, Shift, Test, Color, ColorStandard


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


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]


class EditTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]


class CreateColorStandardForm(forms.ModelForm):
    class Meta:
        model = ColorStandard
        fields = ["name"]


class EditColorStandardForm(forms.ModelForm):
    class Meta:
        model = ColorStandard
        fields = ["name"]


class CreateColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "code", "color_standard"]


class EditColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "code", "color_standard"]
