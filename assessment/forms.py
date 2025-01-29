from django import forms
from .models import Test, Conformity, Assessment, FirstOff, OnProcess, Waste, Viscosity


class CreateAssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = (
            "date",
            "time",
            "shift",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class EditAssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = (
            # "date",
            # "time",
            "shift",
        )

        # widgets = {
        #     "date": forms.DateInput(attrs={"type": "date"}),
        #     "time": forms.TimeInput(attrs={"type": "time"}),
        # }


class FirstOffTestsFrom(forms.ModelForm):
    class Meta:
        model = FirstOff
        fields = (
            "value",
            "remark",
        )
        widgets = {
            "value": forms.RadioSelect(
                attrs={"class": "flex gap-2"},
                choices=[(True, "Pass"), (False, "Fail")],
            ),
        }


class OnProcessConformitiesForm(forms.ModelForm):
    class Meta:
        model = OnProcess
        fields = (
            "conformity",
            "sample_no",
            "date",
            "time",
            "action",
        )

        widgets = {
            "date": forms.TimeInput(attrs={"type": "date"}),
            "conformity": forms.Select(attrs={"style": "width: 10rem"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "sample_no": forms.TextInput(attrs={"style": "width: 10rem"}),
            "action": forms.Textarea(attrs={"rows": 3, "cols": 36}),
        }


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]


class EditTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]


class CreateConformityForm(forms.ModelForm):
    class Meta:
        model = Conformity
        fields = ["name"]


class EditConformityForm(forms.ModelForm):
    class Meta:
        model = Conformity
        fields = ["name"]


class CreateWasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ["quantity"]


class SampleForm(forms.ModelForm):
    class Meta:
        model = Viscosity
        fields = ["sample_no"]

    sample_no = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"style": "width: 12rem"}),
    )


class CreateViscosityForm(forms.Form):
    color_id = forms.IntegerField(widget=forms.HiddenInput())
    color_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )
    color_viscosity = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )
    value = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Viscosity Value",
        widget=forms.NumberInput(attrs={"style": "width: 7rem"}),
    )
