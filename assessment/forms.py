from django import forms
from .models import (
    Test,
    Conformity,
    Assessment,
    FirstOff,
    OnProcess,
    Waste,
    SemiWaste,
    Viscosity,
    Lamination,
    Substrate,
)


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


class CreateSemiWasteForm(forms.ModelForm):
    class Meta:
        model = SemiWaste
        fields = ("tag_no", "quantity", "remark")
        widgets = {
            "tag_no": forms.TextInput(attrs={"style": "width: 12rem"}),
            "quantity": forms.NumberInput(attrs={"style": "width: 12rem"}),
            "remark": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }


class UpdateSemiWasteForm(forms.ModelForm):
    class Meta:
        model = SemiWaste
        fields = ("quantity", "approved_quantity", "comment")

        widgets = {
            "approved_quantity": forms.NumberInput(attrs={"style": "width: 10rem"}),
            "comment": forms.Textarea(attrs={"rows": 3, "cols": 30}),
            "quantity": forms.HiddenInput(),
        }

    quantity = forms.IntegerField(
        required=False,
        disabled=True,
        widget=forms.HiddenInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        approved_quantity = cleaned_data.get("approved_quantity")
        quantity = cleaned_data.get("quantity")
        if approved_quantity and quantity and approved_quantity > quantity:
            raise forms.ValidationError(
                "Approved quantity cannot be greater than the maximum quantity."
            )
        return cleaned_data


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


class CreateLaminationForm(forms.ModelForm):
    class Meta:
        model = Lamination
        fields = (
            "ply_structure",
            "mechanism",
            "mixing_ratio",
            "supplier",
            "adhesive",
            "adhesive_batch_no",
            "hardner",
            "hardner_batch_no",
        )

    ply_structure = forms.IntegerField(
        initial=2,
        max_value=4,
        min_value=2,
        required=True,
        widget=forms.NumberInput(attrs={"style": "width: 11rem"}),
    )


class LaminationSubstratesForm(forms.ModelForm):
    class Meta:
        model = Substrate
        fields = (
            "raw_material",
            "batch_no",
        )
