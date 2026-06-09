from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']