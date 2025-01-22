from django import forms
from .models import RawMaterial, Shift, Color, ColorStandard


class CreateRawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ["no", "name"]


class EditRawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ["no", "name"]


class CreateShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["code", "name"]


class EditShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["code", "name"]


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
