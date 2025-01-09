from django import forms
from .models import FirstOff
from assesment.models import FirstOff as FirstOffTest


class EditFirstOffForm(forms.ModelForm):
    class Meta:
        model = FirstOff
        fields = (
            "date",
            "time",
            "shift",
            "paper",
            "batch_no",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class FirstOffTestsFrom(forms.ModelForm):
    class Meta:
        model = FirstOffTest
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
