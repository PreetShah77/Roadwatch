from django import forms
from .models import CustomUser, Complaint, Employee, Task
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        cleaned_data['password'] = make_password(password)
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_id','issue_type', 'severity', 'description', 'coordinates', 'image', 'location','email']




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type', 'description', 'assigned_employee', 'complaint']



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'role']

