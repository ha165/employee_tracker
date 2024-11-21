from django import forms
from django.contrib.auth.models import User
from .models import Employee, KPI, ReviewCycle, PerformanceReview  # Import your Employee model

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User  # Make sure this is specified
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee  # Make sure this is specified
        fields = ['department', 'position',]  # Adjust fields if needed


class KPICreationForm(forms.ModelForm):
    class Meta:
        model = KPI  # Make sure this is specified
        fields = ['name', 'description', 'target_value', 'unit']



class ReviewCycleForm(forms.ModelForm):
    class Meta:
        model = ReviewCycle
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }



class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['employee', 'kpi', 'review_cycle', 'achieved_value']