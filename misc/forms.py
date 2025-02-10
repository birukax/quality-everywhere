from django import forms
from django_select2 import forms as s2forms
from django.forms import formset_factory, inlineformset_factory
from .models import RawMaterial, Shift, Color, ColorStandard
from main.custom_widgets import ColorWidget


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
        fields = ("name", "colors")
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }

    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            queryset=Color.objects.all(),
            search_fields=[
                "name__icontains",
                "code__icontains",
            ],
            attrs={"class": "w-full text-center h-auto"},
        ),
    )


class EditColorStandardForm(forms.ModelForm):
    class Meta:
        model = ColorStandard
        fields = ["colors"]

    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=s2forms.ModelSelect2MultipleWidget(
            queryset=Color.objects.all(),
            search_fields=[
                "name__icontains",
                "code__icontains",
            ],
            attrs={"class": "w-full text-center h-auto"},
        ),
    )


class CreateColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "code", "viscosity"]


class EditColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "code", "viscosity"]
