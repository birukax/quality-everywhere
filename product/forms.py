from django import forms
from .models import Artwork


class AddArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("file", "code", "approved", "remark")
        widgets = {
            "remark": forms.Textarea(attrs={"rows": "3"}),
        }


class EditArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ("approved", "remark")
