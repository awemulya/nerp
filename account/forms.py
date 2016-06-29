from django import forms
from django.utils.translation import ugettext_lazy as _
from account.models import Account, Category, Party
from app.utils.forms import HTML5BootstrapModelForm, KOModelForm


class AccountForm(HTML5BootstrapModelForm):
    class Meta:
        model = Account
        exclude = ('parent', 'category')


class CategoryForm(HTML5BootstrapModelForm):
    class Meta:
        model = Category
        exclude = ('parent',)


class PartyForm(KOModelForm):
    address = forms.CharField(label=_('Address'), required=False)
    phone_no = forms.CharField(label=_('Phone No.'), required=False)
    pan_no = forms.CharField(label=_('PAN No.'), required=False)

    class Meta:
        model = Party
        exclude = ['account']