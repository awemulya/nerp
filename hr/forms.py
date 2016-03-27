from django import forms
from .models import PaymentRecord, PayrollEntry


class PaymentRowForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = '__all__'


class PayrollEntryForm(forms.ModelForm):
    class Meta:
        model = PayrollEntry
        fields = '__all__'
