from django import forms
from .models import PaymentRecord, PayrollEntry
from django.form.widgets import Select, DateInput, NumberInput, DateTimeInput


class PaymentRowForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = '__all__'

        # fields = ('name', 'title', 'birth_date')
        widgets = {
            'paid_employee': Select(attrs={}),
            'paid_from_date': DateInput(attrs={}),
            'paid_to_date': DateInput(attrs={}),
            'absent_days': NumberInput(attrs={}),
            'allowence': NumberInput(attrs={}),
            'incentive': NumberInput(attrs={}),
            'deduced_amount': NumberInput(attrs={}),
            'paid_amount': NumberInput(attrs={}),
        }


class PayrollEntryForm(forms.ModelForm):
    class Meta:
        model = PayrollEntry
        fields = '__all__'

        widgets = {
            'entry_row': NumberInput(attrs={}),
            'entry_datetime': DateTimeInput(attrs={})
        }
