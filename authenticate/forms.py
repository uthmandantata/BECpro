from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'password1', 'password2')