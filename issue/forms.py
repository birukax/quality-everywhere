from django import forms
from .models import Department, Location, IssueType, Issue, Remark


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
        fields = ("issue_type", "location", "department", "description")
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "3",
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


class CreateRemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "3",
                }
            ),
        }
