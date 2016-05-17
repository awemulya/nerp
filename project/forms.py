from django.core.urlresolvers import reverse_lazy
from django import forms
from app.utils.forms import HTML5BootstrapModelForm
from models import Aid, Project


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