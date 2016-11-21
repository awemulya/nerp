# from django import forms
from hr.models import Employee
from app.utils.forms import HTML5BootstrapModelForm


class EmployeeFilterForm(HTML5BootstrapModelForm):

    class Meta:
        model = Employee
        fields = ('is_active', 'working_branch')
