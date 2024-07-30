from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Client


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=200)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class TelegramIdForm(forms.Form):
    telegram_id = forms.CharField(required=True, max_length=100)

    class Meta:
        model = Client
        fields = ['telegram_id']
