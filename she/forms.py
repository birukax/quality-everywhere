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
    FirePrevention,
    Checkpoint,
    FPChecklist,
)


class CreateLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }


class EditLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("name", "active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "active": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }


class CreateIssueTypeForm(forms.ModelForm):
    class Meta:
        model = IssueType
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }


class EditIssueTypeForm(forms.ModelForm):
    class Meta:
        model = IssueType
        fields = ("name", "active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "active": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }


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
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
        }


class EditIncidentTypeForm(forms.ModelForm):
    class Meta:
        model = IncidentType
        fields = ("name", "active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "active": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }


class CreateIncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = (
            "employee",
            "location",
            "type",
            "referred_to_hospital",
            "date",
            "time",
            "witness_list",
            "cause",
            "body_part_injured",
            "nature_of_injury",
            "pre_incident_activity",
            "tools_used_before_incident",
            "recommendation",
            "action_taken",
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
            "date": forms.DateInput(
                attrs={"class": "w-full text-center h-auto", "type": "date"}
            ),
            "time": forms.TimeInput(
                attrs={"class": "w-full text-center h-auto", "type": "time"}
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
        queryset=Location.objects.filter(active=True),
        widget=s2forms.ModelSelect2Widget(
            model=Location,
            queryset=Location.objects.filter(active=True),
            search_fields=["name__icontains"],
            max_results=5,
            attrs={"class": "w-full text-center h-auto"},
        ),
    )

    type = forms.ModelChoiceField(
        queryset=IncidentType.objects.filter(active=True),
        widget=s2forms.ModelSelect2Widget(
            model=IncidentType,
            queryset=IncidentType.objects.filter(active=True),
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


class CreateCheckpointForm(forms.ModelForm):
    class Meta:
        model = Checkpoint
        fields = ("name",)
        widgets = {
            "name": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "active": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }


class EditCheckpointForm(forms.ModelForm):
    class Meta:
        model = Checkpoint
        fields = ("name", "active")
        widgets = {
            "name": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
            "active": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
        }


class CreateFirePreventionForm(forms.ModelForm):
    class Meta:
        model = FirePrevention
        fields = ("shift",)
        widgets = {
            "shift": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }


class FPChecklistForm(forms.ModelForm):
    class Meta:
        model = FPChecklist
        fields = (
            "value",
            "remark",
        )

        widgets = {
            "value": forms.RadioSelect(
                attrs={"class": " flex text-sm tracking-wider gap-2"},
            ),
            "remark": forms.TextInput(
                attrs={
                    "class": "w-full h-auto",
                }
            ),
        }


class SubmitFPChecklistForm(forms.ModelForm):
    class Meta:
        model = FirePrevention
        fields = ("comment",)
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "2",
                }
            ),
        }
        labels = {"comment": "Comment for the next shift?"}
