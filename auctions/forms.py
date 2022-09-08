from allauth.account.forms import LoginForm, SignupForm
from django import forms
from .models import User


class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'autofocus': 'on', 'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


class SignupForm(SignupForm):
    login = forms.CharField(max_length=24)

    field_order = ["login", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={'autofocus': 'on', 'class': 'form-control', 'autocomplete': 'off', })
        self.fields['email'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
