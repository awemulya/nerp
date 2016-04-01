from django import forms
# from datetime import date
from .models import PaymentRecord, PayrollEntry, BranchOffice
from django.forms.widgets import Select, DateInput, NumberInput, DateTimeInput#, MultiWidget
from njango.fields import BSDateField, today


# class DateSelectorWidget(MultiWidget):
#     def __init__(self, attrs=None):
#         # create choices for days, months, years
#         # example below, the rest snipped for brevity.
#         days = [(day, day) for day in range(1, 30)]
#         years = [(year, year) for year in (2011, 2012, 2013)]
#         months = [(month, month) for month in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)]
#         _widgets = (
#             Select(attrs=attrs, choices=days),
#             Select(attrs=attrs, choices=months),
#             Select(attrs=attrs, choices=years),
#         )
#         super(DateSelectorWidget, self).__init__(_widgets, attrs)

#     def decompress(self, value):
#         if value:
#             return [value.day, value.month, value.year]
#         return [None, None, None]

#     def format_output(self, rendered_widgets):
#         return ''.join(rendered_widgets)

#     def value_from_datadict(self, data, files, name):
#         datelist = [
#             widget.value_from_datadict(data, files, name + '_%s' % i)
#             for i, widget in enumerate(self.widgets)]
#         try:
#             D = date(
#                 day=int(datelist[0]),
#                 month=int(datelist[1]),
#                 year=int(datelist[2]),
#             )
#         except ValueError:
#             return ''
#         else:
#             return str(D)


class PaymentRowForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        # exclude = ('paid_from_date', 'paid_to_date')
        fields = '__all__'

        # fields = ('name', 'title', 'birth_date')
        widgets = {
            'paid_employee': Select(attrs={'data-bind': "value: paid_employee"}),
            'paid_from_date': DateInput(attrs={'data-bind': "value:$parent.paid_to_date"}),
            'paid_to_date': DateInput(attrs={'data-bind': "value:$parent.paid_to_date"}),
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


class GroupPayrollForm(forms.Form):
    payroll_type = forms.ChoiceField(
        choices=[('INDIVIDUAL', 'Individual'),
                 ('BRANCH', 'Branch')],
        widget=Select(attrs={'data-bind': 'value: payroll_type'})
                 )
    branch = forms.ChoiceField(choices=[(o.id, o.name) for o in BranchOffice.objects.all()])
    from_date = forms.DateField(
        widget=DateInput(attrs={
            'data-bind': 'value: paid_from_date',
            'is_required': True
            }),
        )
    to_date = forms.DateField(
        widget=DateInput(attrs={
            'data-bind': 'value: paid_to_date',
            'is_required': True
            }),
        )
