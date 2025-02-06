from django import forms
from .models import Artwork


class AddArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("file", "approved", "code", "remark")
        widgets = {
            "file": forms.FileInput(attrs={"class": "w-full text-center h-8"}),
            "code": forms.TextInput(attrs={"class": "w-full text-center h-8"}),
            "approved": forms.CheckboxInput(attrs={"class": "w-4 h-4"}),
            "remark": forms.Textarea(attrs={"class": "w-full", "rows": "3"}),
        }


class EditArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("approved", "remark")
