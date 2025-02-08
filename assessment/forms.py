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
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "shift": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }


class EditAssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ("shift",)

        widgets = {
            "shift": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            )
        }


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
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "conformity": forms.Select(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "sample_no": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "action": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "3",
                }
            ),
        }


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class EditTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class CreateConformityForm(forms.ModelForm):
    class Meta:
        model = Conformity
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class EditConformityForm(forms.ModelForm):
    class Meta:
        model = Conformity
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class CreateWasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ["quantity"]
        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class CreateSemiWasteForm(forms.ModelForm):
    class Meta:
        model = SemiWaste
        fields = ("tag_no", "quantity", "remark")
        widgets = {
            "tag_no": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "remark": forms.Textarea(
                attrs={
                    "class": "w-full ",
                    "rows": "3",
                }
            ),
        }


class UpdateSemiWasteForm(forms.ModelForm):
    class Meta:
        model = SemiWaste
        fields = ("quantity", "approved_quantity", "comment")

        widgets = {
            "approved_quantity": forms.NumberInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "w-full ",
                    "rows": "3",
                }
            ),
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
        widget=forms.TextInput(
            attrs={
                "class": "w-full items-center text-center h-auto",
            }
        ),
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
        widget=forms.NumberInput(
            attrs={"class": "w-full items-center text-center h-auto"}
        ),
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
        widgets = {
            "mechanism": forms.Select(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "mixing_ratio": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "supplier": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "adhesive": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "adhesive_batch_no": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "hardner": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "hardner_batch_no": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }

    ply_structure = forms.IntegerField(
        initial=2,
        max_value=4,
        min_value=2,
        required=True,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full items-center text-center h-auto",
            }
        ),
    )


class LaminationSubstratesForm(forms.ModelForm):
    class Meta:
        model = Substrate
        fields = (
            "raw_material",
            "batch_no",
        )
