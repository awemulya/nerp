from django import forms
# from datetime import date
from .models import PaymentRecord, PayrollEntry, BranchOffice, Employee
from django.forms.widgets import Select, DateInput, NumberInput, DateTimeInput#, MultiWidget
from njango.fields import BSDateField, today
from django.utils.translation import ugettext_lazy as _
from .models import Deduction, IncentiveName, AllowanceName, Incentive, Allowance, EmployeeAccount, TaxScheme, TaxCalcScheme
import pdb

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


def get_deduction_names():
    deductions = Deduction.objects.all()
    names = []
    for obj in deductions:
        if obj.deduction_for == 'EMPLOYEE ACC':
            name = '_'.join(obj.in_acc_type.name.split(' ')).lower()
        else:
            name = '_'.join(obj.name.split(' ')).lower()
        names.append((name, obj.id))
    return names


def get_incentive_names():
    incentives = IncentiveName.objects.all()
    names = []
    for obj in incentives:
        # if obj.deduction_for == 'EMPLOYEE ACC':
        #     name = obj.in_acc_type.name
        # else:
        #     name = '_'.join(obj.name.split(' ')).lower()
        name = '_'.join(obj.name.split(' ')).lower()
        names.append((name, obj.id))
    return names


def get_allowance_names():
    allowances = AllowanceName.objects.all()
    names = []
    for obj in allowances:
        # if obj.deduction_for == 'EMPLOYEE ACC':
        #     name = obj.in_acc_type.name
        # else:
        #     name = '_'.join(obj.name.split(' ')).lower()
        name = '_'.join(obj.name.split(' ')).lower()
        names.append((name, obj.id))
    return names


class DeductionDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # extra = kwargs.pop('extra')
        super(DeductionDataForm, self).__init__(*args, **kwargs)

        for name, id in get_deduction_names():
            self.fields['deduction_%d' % id] = forms.FloatField(
                label=' '.join(name.split('_')).title(),
                widget=NumberInput(attrs={'data-bind': "value: deduction_%s, readOnly: disable_input" % (id)}),
            )


class IncentiveDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # extra = kwargs.pop('extra')
        super(IncentiveDataForm, self).__init__(*args, **kwargs)

        for name, id in get_incentive_names():
            self.fields['incentive_%d' % id] = forms.FloatField(
                label=' '.join(name.split('_')).title(),
                widget=NumberInput(attrs={'data-bind': "value: incentive_%s, readOnly: disable_input" % (id)}),
            )


class AllowanceDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # extra = kwargs.pop('extra')
        super(AllowanceDataForm, self).__init__(*args, **kwargs)

        for name, id in get_allowance_names():
            self.fields['allowance_%d' % id] = forms.FloatField(
                label=' '.join(name.split('_')).title(),
                widget=NumberInput(attrs={'data-bind': "value: allowance_%s, readOnly: disable_input" % (id)}),
            )


class PaymentRowForm(forms.ModelForm):
    # deduced_amount = forms.FloatField(
    #     widget=NumberInput(attrs={'data-bind': "value: deduced_amount, disable: disable_input"})
    # )

    class Meta:
        model = PaymentRecord
        exclude = ('deduction_detail',)
        # fields = '__all__'

        # fields = ('name', 'title', 'birth_date')
        widgets = {
            'paid_employee': Select(attrs={'data-bind': "value: paid_employee, event:{ change: employee_changed}, readOnly: disable_input, options: $parent.employee_options, optionsText: 'name', optionsValue: 'id', optionsCaption: 'Select Employee',optionsAfterRender: $parent.set_option_disable"}),
            # 'paid_from_date': DateInput(attrs={'data-bind': "value:$parent.paid_from_date, disable: disable_input"}),
            # 'paid_to_date': DateInput(attrs={'data-bind': "value:$parent.paid_to_date, disable: disable_input"}),
            'absent_days': NumberInput(attrs={'data-bind': "visible: false, readOnly: disable_input"}),
            'allowance': NumberInput(attrs={'data-bind': "value: allowance, readOnly: disable_input"}),
            'incentive': NumberInput(attrs={'data-bind': "value: incentive, readOnly: disable_input"}),
            'pf_deduction_amount': NumberInput(attrs={'data-bind': "value: pf_deduction_amount", "step": "any"}),
            'deduced_amount': NumberInput(attrs={'data-bind': "value: deduced_amount, readOnly: disable_input"}),
            'income_tax': NumberInput(attrs={'data-bind': "value: income_tax, readOnly: disable_input"}),
            'pro_tempore_amount': NumberInput(attrs={'data-bind': "value: pro_tempore_amount, readOnly: disable_input"}),
            'salary': NumberInput(attrs={'data-bind': "value: salary, readOnly: disable_input"}),
            'paid_amount': NumberInput(attrs={'data-bind': "value: paid_amount, readOnly: disable_input"}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(PaymentRowForm, self).__init__(*args, **kwargs)
    #     self.fields["paid_employee"].choices = [("", _("Select Employee")),] + list(self.fields["paid_employee"].choices)[1:]


class PayrollEntryForm(forms.ModelForm):
    class Meta:
        model = PayrollEntry
        fields = '__all__'

        widgets = {
            'entry_row': NumberInput(attrs={}),
            'entry_datetime': DateTimeInput(attrs={})
        }


class GroupPayrollForm(forms.Form):
    branch_choices = [(o.id, o.name) for o in BranchOffice.objects.all()]
    branch_choices.insert(0, ('ALL', 'All'))
    payroll_type = forms.ChoiceField(
        choices=[
                 ('INDIVIDUAL', _('Individual')),
                 ('GROUP', _('Group'))],
        widget=Select(attrs={'data-bind': 'value: payroll_type'})
                 )
    branch = forms.ChoiceField(
        choices=branch_choices,
        widget=Select(attrs={'data-bind': 'value: branch'})
        )
    from_date = forms.DateField(
        widget=DateInput(attrs={
            'data-bind': 'value: paid_from_date',
            'placeholder': 'YYYY-MM-DD',
            'is_required': True
            }),
        )
    to_date = forms.DateField(
        widget=DateInput(attrs={
            'data-bind': 'value: paid_to_date',
            'placeholder': 'YYYY-MM-DD',
            'is_required': True
            }),
        )


# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = '__all__'

#     def clean(self):
#         accounts = self.cleaned_data.get('accounts')
#         import pdb
#         pdb.set_trace()

#         return self.cleaned_data

# class EmployeeAccountInlineFormset(forms.models.BaseInlineFormSet):
#     def clean(self):
#         if any(self.errors):
#             return
#         account_types = []
#         bank_account_count = 0
#         cntr = 0
#         for form in self.forms:
#             if form.cleaned_data:
#                 other_account_type = form.cleaned_data['other_account_type']
#                 is_salary_account = form.cleaned_data['is_salary_account']
#                 account_meta_type = form.cleaned_data['account_meta_type']

#                 if account_meta_type == 'BANK_ACCOUNT':
#                     if other_account_type:
#                         raise forms.ValidationError(
#                             _('Employee Bank account cant have account type %s. Should be None type' % other_account_type))
#                     if is_salary_account:
#                         cntr += 1
#                     bank_account_count += 1
#                 else:
#                     if not other_account_type:
#                         raise forms.ValidationError(
#                             _('Employee Other account on account meta type need other account type'))
#                     if is_salary_account:
#                         raise forms.ValidationError(
#                             _('Only Employee bank account be a salary account'))
#                     if other_account_type in account_types:
#                         acc_type_name = _(other_account_type.name)
#                         raise forms.ValidationError(
#                             _('Cannot have more than one type of %s' % acc_type_name))
#                     account_types.append(other_account_type)
#                 if cntr > 1:
#                     raise forms.ValidationError(
#                             _('Cannot have more than one salary account'))
#         if bank_account_count == 0:
#             raise forms.ValidationError(
#                 _('Employee Needs at least one bank account'))

class EmployeeAccountInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        account_types = []
        bank_account_count = 0
        cntr = 0
        for form in self.forms:
            if form.cleaned_data:
                other_account_type = form.cleaned_data['other_account_type']
                is_salary_account = form.cleaned_data['is_salary_account']
                account_meta_type = form.cleaned_data['account_meta_type']

                if account_meta_type == 'BANK_ACCOUNT':
                    if other_account_type:
                        form.add_error(
                            'other_account_type',
                            _('Employee Bank account cant have account type %s. Should be None type' % other_account_type)
                        )
                    if is_salary_account:
                        cntr += 1
                    bank_account_count += 1
                else:
                    if not other_account_type:
                        form.add_error(
                            'other_account_type',
                            _('Employee Other account on account meta type need other account type')
                        )
                    if is_salary_account:
                        form.add_error(
                            'is_salary_account',
                            _('Only Employee bank account be a salary account')
                        )
                    if other_account_type in account_types:
                        acc_type_name = _(other_account_type.name)
                        raise forms.ValidationError(
                            _('Cannot have more than one type of %s' % acc_type_name))
                    account_types.append(other_account_type)
                if cntr > 1:
                    raise forms.ValidationError(
                            _('Cannot have more than one salary account'))
        if bank_account_count == 0:
            raise forms.ValidationError(
                _('Employee Needs at least one bank account'))


class IncentiveInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        # account_types = []
        # bank_account_count = 0
        # cntr = 0
        for form in self.forms:
            if form.cleaned_data:
                sum_type = form.cleaned_data.get("sum_type")
                amount = form.cleaned_data.get("amount")
                amount_rate = form.cleaned_data.get("amount_rate")
                payment_cycle = form.cleaned_data.get("payment_cycle")
                year_payment_cycle_month = form.cleaned_data.get("year_payment_cycle_month")

                if sum_type == 'AMOUNT' and not amount:
                    form.add_error(
                        'amount',
                        'Need amount field to be filled up when Sum Type is Amount'
                    )
                elif sum_type == 'RATE' and not amount_rate:
                    form.add_error(
                        'amount_rate',
                        'Need amount rate field to be filled up when Sum Type is Rate'
                    )
                if payment_cycle == 'Y' and not year_payment_cycle_month:
                    form.add_error(
                        'year_payment_cycle_month',
                        'This field is needed if it is a yearly allowance'
                    )


class AllowanceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        # account_types = []
        # bank_account_count = 0
        # cntr = 0
        for form in self.forms:
            if form.cleaned_data:
                sum_type = form.cleaned_data.get("sum_type")
                amount = form.cleaned_data.get("amount")
                amount_rate = form.cleaned_data.get("amount_rate")
                payment_cycle = form.cleaned_data.get("payment_cycle")
                year_payment_cycle_month = form.cleaned_data.get("year_payment_cycle_month")

                if sum_type == 'AMOUNT' and not amount:
                    form.add_error(
                        'amount',
                        'Need amount field to be filled up when Sum Type is Amount'
                    )
                elif sum_type == 'RATE' and not amount_rate:
                    form.add_error(
                        'amount_rate',
                        'Need amount rate field to be filled up when Sum Type is Rate'
                    )
                if payment_cycle == 'Y' and not year_payment_cycle_month:
                    form.add_error(
                        'year_payment_cycle_month',
                        'This field is needed if it is a yearly allowance'
                    )


class DeductionModelFormSet(forms.BaseModelFormSet):
    def clean(self):
        super(DeductionModelFormSet, self).clean()
        for form in self.forms:
            if form.cleaned_data:
                deduct_type = form.cleaned_data.get("deduct_type")
                amount = form.cleaned_data.get("amount")
                amount_rate = form.cleaned_data.get("amount_rate")

                deduction_for = form.cleaned_data.get("deduction_for")
                explicit_acc = form.cleaned_data.get("explicit_acc")
                in_acc_type = form.cleaned_data.get("in_acc_type")

                if deduct_type == 'AMOUNT' and not amount:
                    form.add_error(
                        'amount',
                        'Need amount field to be filled up when Sum Type is Amount'
                    )
                elif deduct_type == 'RATE' and not amount_rate:
                    form.add_error(
                        'amount_rate',
                        'Need amount rate field to be filled up when Sum Type is Rate'
                    )
                if deduction_for == 'EXPLICIT ACC' and not explicit_acc:
                    form.add_error(
                        'explicit_acc',
                        'This field is required with Deduction for Explicit Account'
                    )
                elif deduction_for == 'EMPLOYEE ACC' and not in_acc_type:
                    form.add_error(
                        'in_acc_type',
                        'This field is required with Deduction for Employee Account'
                    )


# class TaxSchemeModelFormSet(forms.BaseModelFormSet):
#     def clean(self):
#         super(TaxSchemeModelFormSet, self).clean()
        # e_p_dict_list = []
        # for form in self.forms:
        #     if form.cleaned_data:
        #         start_from = form.cleaned_data.get("start_from")
        #         end_to = form.cleaned_data.get("end_to")
        #         priority = form.cleaned_data.get("priority")
        #         DELETE = form.cleaned_data.get("DELETE")

        #         if end_to < start_from:
        #             form.add_error(
        #                 'start_from',
        #                 'start_from must be less than end_to',
        #             )

        #         if not DELETE:
        #             e_p_dict_list.append({
        #                 'start_from': start_from,
        #                 'end_to': end_to,
        #                 'priority': priority,
        #                 'form': form})
        # sorted_dict_list = sorted(
        #     e_p_dict_list,
        #     key=lambda item: item['priority'],
        #     reverse=True
        # )
        # if sorted_dict_list[-1]['start_from'] != 0:
        #     sorted_dict_list[-1]['form'].add_error(
        #         'start_from',
        #         'First range must start from 0',
        #     )
        # for index, item in enumerate(sorted_dict_list):
        #     if index == 0:
        #         if item['end_to'] is not None:
        #             item['form'].add_error(
        #                 'end_to',
        #                 'Last range end to should be None'
        #             )
        #         try:
        #             if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
        #                 item['form'].add_error(
        #                     'start_from',
        #                     'start_from must be just after previous end_to',
        #                 )
        #         except:
        #             pass

        #     else:
        #         if item['end_to'] is None:
        #             item['form'].add_error(
        #                 'end_to',
        #                 'This field should not be None'
        #             )
        #         try:
        #             if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
        #                 item['form'].add_error(
        #                     'start_from',
        #                     'start_from must be just after previous end_to',
        #                 )
        #         except:
        #             pass


class TaxCalcSchemeInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(TaxCalcSchemeInlineFormSet, self).clean()
        e_p_dict_list = []
        for form in self.forms:
            if form.cleaned_data:
                start_from = form.cleaned_data.get("start_from")
                end_to = form.cleaned_data.get("end_to")
                priority = form.cleaned_data.get("priority")
                DELETE = form.cleaned_data.get("DELETE")

                if end_to < start_from:
                    form.add_error(
                        'start_from',
                        'start_from must be less than end_to',
                    )

                if not DELETE:
                    e_p_dict_list.append({
                        'start_from': start_from,
                        'end_to': end_to,
                        'priority': priority,
                        'form': form})
        sorted_dict_list = sorted(
            e_p_dict_list,
            key=lambda item: item['priority'],
            reverse=True
        )
        if sorted_dict_list[-1]['start_from'] != 0:
            sorted_dict_list[-1]['form'].add_error(
                'start_from',
                'First range must start from 0',
            )
        for index, item in enumerate(sorted_dict_list):
            if index == 0:
                if item['end_to'] is not None:
                    item['form'].add_error(
                        'end_to',
                        'Last range end to should be None'
                    )
                try:
                    if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
                        item['form'].add_error(
                            'start_from',
                            'start_from must be just after previous end_to',
                        )
                except:
                    pass

            else:
                if item['end_to'] is None:
                    item['form'].add_error(
                        'end_to',
                        'This field should not be None'
                    )
                try:
                    if item['start_from'] != sorted_dict_list[index + 1]['end_to'] + 1:
                        item['form'].add_error(
                            'start_from',
                            'start_from must be just after previous end_to',
                        )
                except:
                    pass



class AllowanceForm(forms.ModelForm):

    class Meta:
        model = Allowance
        fields = '__all__'

    def clean(self):
        cleaned_data = super(AllowanceForm, self).clean()
        sum_type = cleaned_data.get("sum_type")
        amount = cleaned_data.get("amount")
        amount_rate = cleaned_data.get("amount_rate")
        payment_cycle = cleaned_data.get("payment_cycle")
        year_payment_cycle_month = cleaned_data.get("year_payment_cycle_month")

        if sum_type == 'AMOUNT' and not amount:
            self.add_error(
                'amount',
                'Need amount field to be filled up when Sum Type is Amount'
            )
        elif sum_type == 'RATE' and not amount_rate:
            self.add_error(
                'amount_rate',
                'Need amount rate field to be filled up when Sum Type is Rate'
            )
        if payment_cycle == 'Y' and not year_payment_cycle_month:
            self.add_error(
                'year_payment_cycle_month',
                'This field is needed if it is a yearly allowance'
            )


class IncentiveForm(forms.ModelForm):

    class Meta:
        model = Incentive
        fields = '__all__'

    def clean(self):
        cleaned_data = super(IncentiveForm, self).clean()
        sum_type = cleaned_data.get("sum_type")
        amount = cleaned_data.get("amount")
        amount_rate = cleaned_data.get("amount_rate")
        payment_cycle = cleaned_data.get("payment_cycle")
        year_payment_cycle_month = cleaned_data.get("year_payment_cycle_month")

        if sum_type == 'AMOUNT' and not amount:
            self.add_error(
                'amount',
                'Need amount field to be filled up when Sum Type is Amount'
            )
        elif sum_type == 'RATE' and not amount_rate:
            self.add_error(
                'amount_rate',
                'Need amount rate field to be filled up when Sum Type is Rate'
            )
        if payment_cycle == 'Y' and not year_payment_cycle_month:
            self.add_error(
                'year_payment_cycle_month',
                'This field is needed if it is a yearly allowance'
            )


class DeductionForm(forms.ModelForm):

    class Meta:
        model = Deduction
        fields = '__all__'

    def clean(self):
        cleaned_data = super(DeductionForm, self).clean()
        sum_type = cleaned_data.get("sum_type")
        amount = cleaned_data.get("amount")
        amount_rate = cleaned_data.get("amount_rate")

        deduction_for = cleaned_data.get("deduction_for")
        explicit_acc = cleaned_data.get("explicit_acc")
        in_acc_type = cleaned_data.get("in_acc_type")

        if sum_type == 'AMOUNT' and not amount:
            self.add_error(
                'amount',
                'Need amount field to be filled up when Sum Type is Amount'
            )
        elif sum_type == 'RATE' and not amount_rate:
            self.add_error(
                'amount_rate',
                'Need amount rate field to be filled up when Sum Type is Rate'
            )
        if deduction_for == 'EXPLICIT ACC' and not explicit_acc:
            self.add_error(
                'explicit_acc',
                'This field is required with Deduction for Explicit Account'
            )
        elif deduction_for == 'EMPLOYEE ACC' and not in_acc_type:
            self.add_error(
                'in_acc_type',
                'This field is required with Deduction for Employee Account'
            )


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        # fields = '__all__'
        exclude = ('accounts',)


class IncentiveNameForm(forms.ModelForm):

    class Meta:
        model = IncentiveName
        fields = '__all__'


class AllowanceNameForm(forms.ModelForm):

    class Meta:
        model = AllowanceName
        fields = '__all__'


class TaxSchemeForm(forms.ModelForm):

    class Meta:
        model = TaxScheme
        fields = '__all__'
        # exclude = ('accounts',)

# class EmployeeAccountForm(forms.ModelForm):

#     class Meta:
#         model = EmployeeAccount
#         exclude = ('employee',)
#         # fields = '__all__'

    # def clean(self):
    #     cleaned_data = super(EmployeeAccountForm, self).clean()
    #     other_account_type = cleaned_data['other_account_type']
    #     is_salary_account = cleaned_data['is_salary_account']
    #     account_meta_type = cleaned_data['account_meta_type']

    #     if account_meta_type == 'BANK_ACCOUNT':
    #         if other_account_type:
    #             self.add_error(
    #                 'other_account_type',
    #                 _('Employee Bank account cant have account type %s. Should be None type' % other_account_type)
    #             )
    #     else:
    #         if not other_account_type:
    #             self.add_error(
    #                 'other_account_type',
    #                 _('Employee Other account on account meta type need other account type')
    #             )
    #         if is_salary_account:
    #             self.add_error(
    #                 'is_salary_account',
    #                 _('Only Employee bank account be a salary account')
    #             )


# These are forms for payroll entry
PaymentRowFormSet = forms.formset_factory(PaymentRowForm)
DeductionFormSet = forms.formset_factory(DeductionDataForm)
IncentiveFormSet = forms.formset_factory(IncentiveDataForm)
AllowanceFormSet = forms.formset_factory(AllowanceDataForm)


# These are crud formset
EmployeeAccountFormSet = forms.inlineformset_factory(
    Employee,
    EmployeeAccount,
    extra=1,
    fields='__all__',
    formset=EmployeeAccountInlineFormset
)
IncentiveNameFormSet = forms.inlineformset_factory(
    IncentiveName,
    Incentive,
    extra=1,
    exclude=('account',),
    formset=IncentiveInlineFormset
)
AllowanceNameFormSet = forms.inlineformset_factory(
    AllowanceName,
    Allowance,
    extra=1,
    exclude=('account',),
    formset=AllowanceInlineFormset
)

DeductionDetailFormSet = forms.modelformset_factory(
    Deduction,
    extra=1,
    can_delete=True,
    exclude=('account',),
    formset=DeductionModelFormSet
)

# TaxSchemeFormSet = forms.modelformset_factory(
#     TaxScheme,
#     can_delete=True,
#     extra=1,
#     fields='__all__',
#     formset=TaxSchemeModelFormSet
# )

TaxCalcSchemeFormSet = forms.inlineformset_factory(
    TaxScheme,
    TaxCalcScheme,
    extra=1,
    fields='__all__',
    formset=TaxCalcSchemeInlineFormSet
)
