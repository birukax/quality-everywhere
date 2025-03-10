from django import forms
from django_select2 import forms as s2forms
from .models import (
    Department,
    Location,
    IssueType,
    Issue,
    Remark,
    IncidentType,
    Incident,
    Employee,
)


class CreateLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("name",)


class CreateIssueTypeForm(forms.ModelForm):
    class Meta:
        model = IssueType
        fields = ("name",)


class CreateIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (
            "issue_type",
            "location",
            "department",
            "observation",
            "suggestion",
            "image",
        )
        widgets = {
            "observation": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "suggestion": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
        }

    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(active=True),
        widget=forms.Select(attrs={"class": "w-full items-center text-center h-auto"}),
    )
    issue_type = forms.ModelChoiceField(
        queryset=IssueType.objects.filter(active=True),
        widget=forms.Select(attrs={"class": "w-full items-center text-center h-auto"}),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(active=True),
        widget=forms.Select(attrs={"class": "w-full items-center text-center h-auto"}),
    )


class CreateIncidentTypeForm(forms.ModelForm):
    class Meta:
        model = IncidentType
        fields = ("name",)


class CreateIncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = (
            "employee",
            "location",
            "date",
            "time",
            "witness_list",
            "referred_to_hospital",
            "cause",
            "body_part_injured",
            "nature_of_injury",
            "pre_incident_activity",
            "tools_used_before_incident",
            "recommendation",
            "action_taken",
            "incident_type",
        )
        labels = {
            "employee": "Employee",
            "location": "Location",
            "date": "Date",
            "time": "Time",
            "witness_list": "Witness List",
            "referred_to_hospital": "Referred to Hospital",
            "cause": "What caused the incident?",
            "body_part_injured": "What body part was injured?",
            "nature_of_injury": "What was the nature of the injury?",
            "pre_incident_activity": "What was the employee doing prior to the incident?",
            "tools_used_before_incident": "What equipment, tools were being used?",
            "recommendation": "What are your Recommendations regarding the incident?",
            "action_taken": "What action was taken?",
            "incident_type": "Incident Type?",
        }
        widgets = {
            "location": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "referred_to_hospital": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
            "cause": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "body_part_injured": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "nature_of_injury": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "pre_incident_activity": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "tools_used_before_incident": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "recommendation": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "action_taken": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
        }

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(status="Active"),
        widget=s2forms.ModelSelect2Widget(
            model=Employee,
            queryset=Employee.objects.filter(status="Active"),
            search_fields=["name__icontains"],
            max_results=5,
            attrs={"class": "w-full text-center h-auto"},
        ),
    )

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=s2forms.ModelSelect2Widget(
            model=Location,
            queryset=Location.objects.all(),
            search_fields=["name__icontains"],
            max_results=5,
            attrs={"class": "w-full text-center h-auto"},
        ),
    )

    incident_type = forms.ModelChoiceField(
        queryset=IncidentType.objects.all(),
        widget=s2forms.ModelSelect2Widget(
            model=IncidentType,
            queryset=IncidentType.objects.all(),
            search_fields=["name__icontains"],
            max_results=5,
            attrs={"class": "w-full text-center h-auto"},
        ),
    )
    witness_list = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.filter(status="Active"),
        widget=s2forms.ModelSelect2MultipleWidget(
            model=Employee,
            queryset=Employee.objects.filter(status="Active"),
            max_results=5,
            search_fields=["name__icontains"],
            attrs={"class": "w-full text-center h-auto"},
        ),
    )


class CreateRemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
        }
