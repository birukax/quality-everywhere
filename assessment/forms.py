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
from misc.models import RawMaterial
from job.models import JobTest
from machine.models import Machine, Route, MachineRoute


class CreateAssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = (
            # "date",
            # "time",
            "shift",
        )
        widgets = {
            #     "date": forms.DateInput(
            #         attrs={
            #             "type": "date",
            #             "class": "w-full items-center text-center h-auto",
            #         }
            #     ),
            #     "time": forms.TimeInput(
            #         attrs={
            #             "type": "time",
            #             "class": "w-full items-center text-center h-auto",
            #         }
            #     ),
            "shift": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }


class AddAssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = (
            "shift",
            "machine",
            "reason",
        )
        widgets = {
            "shift": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "machine": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "3",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        job_id = kwargs.pop("job_id")
        super(AddAssessmentForm, self).__init__(*args, **kwargs)
        machines = MachineRoute.objects.filter(
            route=JobTest.objects.filter(id=job_id).first().route
        ).values_list("machine", flat=True)
        self.fields["machine"].queryset = Machine.objects.filter(id__in=machines)


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
                attrs={"class": "flex text-sm tracking-wider gap-2"},
            ),
            "remark": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class OnProcessConformitiesForm(forms.ModelForm):
    class Meta:
        model = OnProcess
        fields = (
            "conformity",
            "sample_no",
            "action",
        )

        widgets = {
            "conformity": forms.Select(
                attrs={
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
        fields = ("name", "critical")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "critical": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }


class EditTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ("name", "critical")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "critical": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
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
            "type",
            "mixing_ratio",
            "supplier",
            "adhesive",
            "adhesive_batch_no",
            "hardner",
            "hardner_batch_no",
        )
        widgets = {
            "type": forms.Select(
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
        widgets = {
            "raw_material": forms.Select(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
            "batch_no": forms.TextInput(
                attrs={
                    "class": "w-full items-center text-center h-auto",
                }
            ),
        }


class BaseLaminationSubstrateFormset(forms.BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        raw_materials = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                raw_material = form.cleaned_data["raw_material"]
                if raw_material in raw_materials or Substrate.objects.filter(
                    lamination=form.instance.lamination, raw_material=raw_material
                ):
                    duplicates = True
                    form.add_error(
                        "raw_material", "Duplicate raw materials are not allowed."
                    )
                raw_materials.append(raw_material)
