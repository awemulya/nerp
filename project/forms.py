from django.core.urlresolvers import reverse_lazy
from django import forms
from app.utils.forms import HTML5BootstrapModelForm
from models import Aid


class AidForm(HTML5BootstrapModelForm):
    class Meta:
        model = Aid
        fields = '__all__'
        widgets = {
            'donor': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('donor_add')}),
            'type': forms.Select(attrs={'class': 'selectize'}),
            'project': forms.Select(attrs={'class': 'selectize'}),
        }