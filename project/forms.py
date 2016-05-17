from django.core.urlresolvers import reverse_lazy
from django import forms
from app.utils.forms import HTML5BootstrapModelForm
from models import Aid, Project, ExpenseCategory, Expense


class AidForm(HTML5BootstrapModelForm):
    class Meta:
        model = Aid
        fields = '__all__'
        widgets = {
            'donor': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('donor_add')}),
            'project': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('project_add')}),
            'type': forms.Select(attrs={'class': 'selectize'}),
        }


class ProjectForm(HTML5BootstrapModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class ExpenseCategoryForm(HTML5BootstrapModelForm):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
        widgets = {
            'project': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('project_add')}),
        }


class ExpenseForm(HTML5BootstrapModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'selectize multi', 'data-url': reverse_lazy('expense_category_add'), 'multiple':'true'}),

            'project': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('project_add')}),
        }