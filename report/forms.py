from django import forms
from django_select2 import forms as s2forms
from .models import ReportHeader
from machine.models import Machine


class CreateReportHeaderForm(forms.ModelForm):
    class Meta:
        model = ReportHeader
        fields = ("report", "effective_date", "issue_no", "machine", "no")
        widgets = {
            "report": forms.Select(attrs={"class": "w-full text-center h-auto"}),
            "no": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "issue_no": forms.NumberInput(attrs={"class": "w-full text-center h-auto"}),
            "effective_date": forms.DateInput(
                attrs={"class": "w-full text-center h-auto", "type": "date"}
            ),
        }
        labels = {
            "report": "Report Type",
            "effective_date": "Effective Date",
            "issue_no": "Issue No",
            "no": "Document No",
            "machine": "Machine",
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
        issue_no = cleaned_data.get("issue_no")
        effective_date = cleaned_data.get("effective_date")
        last_effective_dates = ReportHeader.objects.filter(report=report).order_by(
            "-issue_no"
        )
        machine = cleaned_data.get("machine")
        if report in ["FIRST-OFF", "ON-PROCESS"]:
            if machine is None:
                self.add_error(
                    "machine",
                    f"Machine can't be empty for {report} report",
                )
        else:
            if ReportHeader.objects.filter(report=report, issue_no=issue_no).exists():
                self.add_error(
                    "report", f"{report} with issue no {issue_no} already exists"
                )
        if ReportHeader.objects.filter(
            report=report, effective_date=effective_date
        ).exists():
            self.add_error(
                "effective_date",
                f"{report} with effective date {effective_date} already exists",
            )
        if issue_no < 1:
            self.add_error("issue_no", "Issue no can't be less than 1")
        if last_effective_dates.exists():
            if effective_date < last_effective_dates.first().effective_date:
                self.add_error(
                    "effective_date",
                    f"Effective date can't be less than {last_effective_dates.first().effective_date}",
                )
        return cleaned_data


class EditReportHeaderForm(forms.ModelForm):
    class Meta:
        model = ReportHeader
        fields = ("no",)
        widgets = {
            "no": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }
