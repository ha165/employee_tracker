from django import forms
from django.contrib.auth.models import User
from .models import Employee  # Import your Employee model

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User  # Make sure this is specified
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee  # Make sure this is specified
        fields = ['department', 'position',]  # Adjust fields if needed
