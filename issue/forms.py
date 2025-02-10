from django import forms
from .models import Location, IssueType, Issue, Remark


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
        fields = ("issue_type", "location", "description")
        widgets = {
            "issue_type": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "location": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "rows": "3",
                }
            ),
        }


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
