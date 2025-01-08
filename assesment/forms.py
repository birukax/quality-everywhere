from django import forms
from .models import Test, Conformity


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]


class EditTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]


class CreateConformityForm(forms.ModelForm):
    class Meta:
        model = Conformity
        fields = ["name"]


class EditConformityForm(forms.ModelForm):
    class Meta:
        model = Conformity
        fields = ["name"]
