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


class CreateRemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ("text",)
