from django import forms
from .models import Machine, Color, ColorStandard


class CreateMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'tests']
        

class EditMachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['tests']