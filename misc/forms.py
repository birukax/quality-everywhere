from django import forms
from django.forms import formset_factory
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
        fields = ["name"]


class ColorSelectForm(forms.Form):
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        required=False,
    )


ColorFormSet = formset_factory(ColorSelectForm, extra=8, max_num=8, min_num=8)


class BaseColorFormset(ColorFormSet):
    def clean(self):
        if any(self.errors):
            return
        colors = []
        for form in self.forms:
            color = form.cleaned_data.get("color")
            if color:
                if color in colors:
                    raise forms.ValidationError("Colors must be unique")
                colors.append(color)
        if not colors:
            raise forms.ValidationError("At least on color must be selected")


class EditColorStandardForm(forms.ModelForm):
    class Meta:
        model = ColorStandard
        fields = ["name", "colors"]
        widgets = {
            "colors": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        }


class CreateColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "code", "viscosity"]


class EditColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "code", "viscosity"]
