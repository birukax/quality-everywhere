from django import forms
from .models import QualityTest
from assesment.models import FirstOff


class EditQualityTestForm(forms.ModelForm):
    class Meta:
        model = QualityTest
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
                choices=[(True, "Yes"), (False, "No")],
            ),
        }
