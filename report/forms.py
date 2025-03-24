from django import forms
from django_select2 import forms as s2forms
from .models import ReportHeader
from machine.models import Machine


class CreateReportHeaderForm(forms.ModelForm):
    class Meta:
        model = ReportHeader
        fields = ("report", "machine", "no")
        widgets = {
            "report": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "no": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }

    machine = forms.ModelChoiceField(
        required=False,
        queryset=Machine.objects.all(),
        widget=s2forms.ModelSelect2Widget(
            model=Machine,
            max_results=4,
            search_fields=["name__icontains"],
            attrs={"class": "w-full text-center h-auto"},
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        report = cleaned_data.get("report")
        machine = cleaned_data.get("machine")
        if report in ["FIRST-OFF", "ON-PROCESS"]:
            if machine is None:
                self.add_error(
                    "machine",
                    f"Machine can't be empty for {report} report",
                )
        return cleaned_data


class EditReportHeaderForm(forms.ModelForm):
    class Meta:
        model = ReportHeader
        fields = ("no",)
        widgets = {
            "no": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }
