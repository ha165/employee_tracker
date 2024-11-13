from django import forms
from django.contrib.auth.models import User
from .models import Employee

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class meta :
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

class EmloyeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['department', 'position', 'date_joined','user']