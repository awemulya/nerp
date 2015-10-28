from django import forms

from app.utils.forms import KOModelForm, UserModelChoiceField

from models import Item, Category, Demand, PurchaseOrder, InventoryAccount, Handover, EntryReport, Depreciation, \
    ItemLocation, ItemInstance, InstanceHistory, Expense

from users.models import User
from django.utils.translation import ugettext_lazy as _


class DepreciationForm(KOModelForm):
    class Meta:
        model = Depreciation
        fields = ('depreciate_type', 'depreciate_value', 'time', 'time_type')


class ItemForm(KOModelForm):
    # category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)
    name = forms.CharField(label=_('Name'))
    description = forms.Field(label=_('Specification'), widget=forms.Textarea(), required=False)
    unit = forms.CharField(label=_('Unit'))
    property_classification_reference_number = forms.CharField(label=_('Inventory Classification Reference No.'),
                                                               required=False)
    account_no = forms.Field(widget=forms.TextInput(), label=_('Inventory Account No.'))
    opening_balance = forms.Field(widget=forms.TextInput(), initial=0, label=_('Opening Balance'))
    opening_rate = forms.Field(widget=forms.TextInput(), initial=0, label=_('Opening Rate'))
    opening_rate_vattable = forms.Field(widget=forms.CheckboxInput(attrs={'class': 'inline'}), initial=True,
                                        label=_('Opening Rate Vattable?'), )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ItemForm, self).__init__(*args, **kwargs)
        # self.fields['vattable'].label = _('Vattable')
        self.fields['type'].label = _('Type')
        if self.instance.account:
            self.fields['account_no'].initial = self.instance.account.account_no
        else:
            self.fields['account_no'].initial = InventoryAccount.get_next_account_no()
        if not self.user.in_group('Store Keeper'):
            self.fields['account_no'].widget = forms.HiddenInput()
            self.fields['opening_balance'].widget = forms.HiddenInput()
            self.fields['property_classification_reference_number'].widget = forms.HiddenInput()
        if self.instance.id:
            self.fields['opening_balance'].widget = forms.HiddenInput()
            # self.fields['account_no'].widget = forms.HiddenInput()

    def clean_account_no(self):
        if not self.cleaned_data['account_no'].isdigit():
            raise forms.ValidationError("The account no. must be a number.")
        try:
            existing = InventoryAccount.objects.get(account_no=self.cleaned_data['account_no'])
            if self.instance.account.id is not existing.id:
                raise forms.ValidationError("The account no. " + str(
                    self.cleaned_data['account_no']) + " is already in use.")
            return self.cleaned_data['account_no']
        except InventoryAccount.DoesNotExist:
            return self.cleaned_data['account_no']

    class Meta:
        model = Item
        exclude = ['account', 'code', 'category', 'other_properties', 'depreciation']


class CategoryForm(KOModelForm):
    class Meta:
        model = Category
        exclude = ()

        # def clean(self):
        # """ This is the form's clean method, not a particular field's clean method """
        # cleaned_data = self.cleaned_data
        #
        # name = cleaned_data.get('name')
        #
        #     if Category.objects.filter(name=name, company=self.company).count() > 0:
        #         raise forms.ValidationError("Category name already exists.")
        #
        #     # Always return the full collection of cleaned data.
        #     return cleaned_data


class DemandForm(KOModelForm):
    demandee = UserModelChoiceField(User.objects.all(), empty_label=None)

    class Meta:
        model = Demand
        exclude = ()


class PurchaseOrderForm(KOModelForm):
    class Meta:
        model = PurchaseOrder
        exclude = ()


class HandoverForm(KOModelForm):
    class Meta:
        model = Handover
        exclude = ()


class EntryReportForm(KOModelForm):
    class Meta:
        model = EntryReport
        exclude = ()


class ItemLocationForm(KOModelForm):
    class Meta:
        model = ItemLocation
        fields = '__all__'


class ItemInstanceForm(KOModelForm):
    class Meta:
        model = ItemInstance
        fields = '__all__'
        exclude = ['source', 'other_properties']


class ItemInstanceEditForm(KOModelForm):
    class Meta:
        model = ItemInstance
        exclude = ['item', 'source', 'other_properties']


class InstanceHistoryForm(KOModelForm):
    # def save(self, commit=True):
    #     import ipdb
    #     ipdb.set_trace()
    #     ret = super(InstanceHistoryForm, self).save()

    def clean(self):
        cleaned_data = super(InstanceHistoryForm, self).clean()
        if self.instance.from_location == cleaned_data.get('to_location') and self.instance.from_user == cleaned_data.get(
                'to_user'):
            raise forms.ValidationError('Item location and user unchanged.')

    class Meta:
        model = InstanceHistory
        exclude = ['instance', 'from_location', 'from_user']
        fields = '__all__'

class ExpenseForm(KOModelForm):
    class Meta:
        model = Expense
        exclude = ['instance',]