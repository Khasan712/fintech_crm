from django import forms
from apps.v1.user.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(help_text='Enter Password', required=True)
    password2 = forms.CharField(help_text='Enter Password', required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2')
