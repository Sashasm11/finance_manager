from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин или Email')
