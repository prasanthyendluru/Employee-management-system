from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Task

class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'manager':
            user.is_manager = True
        elif user_type == 'employee':
            user.is_employee = True
        if commit:
            user.save()
        return user

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_employee=True)

class TaskStatusForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)

    class Meta:
        model = Task
        fields = ['status']