from django import forms
from .models import Artwork


class AddArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("file", "code", "approved", "remark")
        widgets = {
            "code": forms.TextInput(attrs={"class": "w-full text-center h-auto"}),
            "approved": forms.Select(
                attrs={"class": "w-full text-center h-auto"},
                choices=(((False, "No"), (True, "Yes"))),
            ),
            "remark": forms.Textarea(attrs={"class": "w-full", "rows": "3"}),
        }


class EditArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("approved", "remark")
        widgets = {
            "remark": forms.Textarea(attrs={"class": "w-full", "rows": "3"}),
        }
