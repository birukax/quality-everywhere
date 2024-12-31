from django import forms
from .models import FirstOffApproval

class FirstOffApprovalForm(forms.ModelForm):
    class Meta:
        model = FirstOffApproval
        fields = (
            "approved",
            "comment",
        )
        widgets = {
            'approved': forms.Select(
                attrs={"class": "flex gap-2"},
                choices=[(True, "Approve"), (False, "Reject")],
            ),
        }