from django import forms
from .models import Test, Conformity, Assessment, FirstOff, OnProcess
from machine.models import Machine


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
            "date",
            "time",
            "shift",
        )

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
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
            "time",
            "action",
        )

    def __init__(self, machine=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comformity"].queryset = Machine.objects.get(
            id=machine.id
        ).conformities.all()


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
