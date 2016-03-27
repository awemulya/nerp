from django import forms
from .models import PaymentRecord


class EntryForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = '__all__'
