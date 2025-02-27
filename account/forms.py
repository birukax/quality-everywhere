from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from issue.models import Department
from .models import Profile, ROLES


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }
        labels = {
            "username": "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
        }

    role = forms.ChoiceField(
        choices=ROLES,
        initial=ROLES[0][0],
        widget=forms.Select(attrs={"class": "w-full items-center text-center h-auto"}),
    )
    department = forms.ModelChoiceField(
        required=False,
        queryset=Department.objects.filter(active=True),
        widget=forms.Select(attrs={"class": "w-full items-center text-center h-auto"}),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "w-full items-center text-center h-auto"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "w-full items-center text-center h-auto"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "is_active",
            "first_name",
            "last_name",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }
        labels = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "role",
            "department",
        )
        widgets = {
            "role": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "department": forms.Select(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }
        labels = {
            "role": "Role",
            "department": "Department",
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "w-full items-center text-center h-auto"}
            ),
        }
        labels = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
        }
