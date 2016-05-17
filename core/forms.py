from django import forms
from app.utils.forms import KOModelForm, HTML5BootstrapModelForm
from core.models import Party, Employee, Donor
from django.utils.translation import ugettext_lazy as _


class PartyForm(KOModelForm):
    address = forms.CharField(label=_('Address'), required=False)
    phone_no = forms.CharField(label=_('Phone No.'), required=False)
    pan_no = forms.CharField(label=_('PAN No.'), required=False)

    class Meta:
        model = Party
        exclude = ['account']


class EmployeeForm(KOModelForm):
    class Meta:
        model = Employee
        exclude = ['account']


class DonorForm(HTML5BootstrapModelForm):
    class Meta:
        model = Donor
        fields = ('name',)
