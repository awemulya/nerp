from django import forms
# from datetime import date
from mptt.forms import TreeNodeChoiceField
from njango.nepdate import bs2ad

from hr.bsdate import BSDate
from hr.fields import HRBSFormField, HRBSDateFormField
from hr.helpers import bs_str2tuple
from .models import PaymentRecord, PayrollEntry, BranchOffice, Employee, ReportHR, EmployeeGrade, EmployeeGradeGroup, \
    Designation, ReportTable, DeductionName, GradeScaleValidity, AllowanceValidity, DeductionValidity, PayrollConfig
from django.forms.widgets import Select, DateInput, NumberInput, DateTimeInput, TextInput  # , MultiWidget
from njango.fields import BSDateField, today
from django.utils.translation import ugettext_lazy as _
from .models import Deduction, IncentiveName, AllowanceName, Incentive, Allowance, EmployeeAccount, TaxScheme, \
    TaxCalcScheme, MaritalStatus
from account.models import Account
from app.utils.forms import HTML5BootstrapModelForm
import datetime


# Start Validity Forms
class GradeScaleValidityForm(HTML5BootstrapModelForm):
    class Meta:
        model = GradeScaleValidity
        fields = '__all__'

        widgets = {
            'valid_from': HRBSFormField(attrs={'data-bind': "value: valid_from"}),
            'note': TextInput(attrs={'data-bind': "value: note",})
        }


class AllowanceValidityForm(HTML5BootstrapModelForm):
    class Meta:
        model = AllowanceValidity
        fields = '__all__'
        widgets = {
            'valid_from': HRBSFormField(attrs={'data-bind': "value: valid_from"}),
            'note': TextInput(attrs={'data-bind': "value: note", })
        }


class DeductionValidityForm(HTML5BootstrapModelForm):
    class Meta:
        model = DeductionValidity
        fields = '__all__'

        widgets = {
            'valid_from': HRBSFormField(attrs={'data-bind': "value: valid_from"}),
            'note': TextInput(attrs={'data-bind': "value: note",})
        }


# End Validity Forms

class PayrollEntryForm(HTML5BootstrapModelForm):
    class Meta:
        model = PayrollEntry
        fields = '__all__'

        widgets = {
            'entry_row': NumberInput(attrs={}),
            'entry_datetime': DateTimeInput(attrs={})
        }


class GroupPayrollForm(forms.Form):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(GroupPayrollForm, self).__init__(*args, **kwargs)
        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.fields['branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.fields['branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)

    payroll_type = forms.ChoiceField(
        choices=[
            ('INDIVIDUAL', _('Individual')),
            ('GROUP', _('Group'))],
        widget=Select(attrs={'data-bind': 'value: payroll_type, selectize:{}'})
    )
    branch = TreeNodeChoiceField(
        queryset=BranchOffice.objects.all(),
        widget=Select(attrs={'data-bind': 'value: branch, selectize:{}'})
    )
    from_date = HRBSDateFormField(
        widget=HRBSFormField(attrs={
            'data-bind': 'value: paid_from_date',
            'class': 'td-input-calendar',
            'placeholder': 'YYYY-MM-DD',
            'is_required': True
        }),
    )
    to_date = HRBSDateFormField(
        widget=HRBSFormField(attrs={
            'data-bind': 'value: paid_to_date',
            'class': 'td-input-calendar',
            'placeholder': 'YYYY-MM-DD',
            'is_required': True
        }),
    )


class GetReportForm(forms.Form):
    report = forms.ModelChoiceField(queryset=ReportHR.objects.all())
    from_date = forms.CharField(
        widget=TextInput(attrs={
            'placeholder': 'YYYY-MM-DD',
        }),
    )
    to_date = forms.CharField(
        widget=TextInput(attrs={
            'placeholder': 'YYYY-MM-DD',
        }),
    )
    branch = forms.ModelChoiceField(
        queryset=BranchOffice.objects.all(),
        required=False
    )

    def clean(self):
        cleaned_data = super(GetReportForm, self).clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if self.calendar == 'AD':
            try:
                # Validate it for bsdate
                cleaned_data['from_date'] = datetime.datetime.strptime(
                    from_date, '%Y-%m-%d').date()
            except:
                self.add_error('from_date', _('AD- Incorrect From Date'))
            try:
                cleaned_data['to_date'] = datetime.datetime.strptime(
                    to_date, '%Y-%m-%d').date()
            except:
                self.add_error('to_date', _('AD- Incorrect To Date'))

        else:
            try:

                from_bs_date_as_tuple = BSDate(*bs_str2tuple(
                    from_date
                )).date_tuple()
                cleaned_data['from_date'] = datetime.date(*bs2ad(from_bs_date_as_tuple))

            except:
                # error['paid_from_date'] = 'Incorrect BS Date'
                self.add_error('from_date', _('BS- Incorrect From Date'))
            try:
                to_bs_date_as_tuple = BSDate(*bs_str2tuple(
                    to_date
                )).date_tuple()
                cleaned_data['to_date'] = datetime.date(*bs2ad(to_bs_date_as_tuple))
            except:
                self.add_error('to_date', _('BS- Incorrect To date'))

    def __init__(self, *args, **kwargs):
        if 'calendar' in kwargs.keys():
            self.calendar=kwargs.pop('calendar')
        super(GetReportForm, self).__init__(*args, **kwargs)


class EmployeeAccountInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            account_categories = []
            if form.cleaned_data:
                employee_acc = form.cleaned_data['account']
                account_category = employee_acc.category
                if account_category in account_categories:
                    raise forms.ValidationError(
                        _('All accont category should be unique to each other'))
                account_categories.append(
                    account_category
                )


class IncentiveInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                payment_cycle = form.cleaned_data.get("payment_cycle")
                year_payment_cycle_month = form.cleaned_data.get(
                    "year_payment_cycle_month")

                if payment_cycle == 'Y' and not year_payment_cycle_month:
                    form.add_error(
                        'year_payment_cycle_month',
                        _('This field is needed if it is a yearly allowance')
                    )


class AllowanceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
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


class TaxSchemeInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(TaxSchemeInlineFormSet, self).clean()
        e_p_dict_list = []
        for form in self.forms:
            if form.cleaned_data:
                start_from = form.cleaned_data.get("start_from")
                end_to = form.cleaned_data.get("end_to")
                priority = form.cleaned_data.get("priority")
                DELETE = form.cleaned_data.get("DELETE")

                if end_to:
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
        # sorted_dict_list = sorted(
        #     e_p_dict_list,
        #     key=lambda item: item['priority'],
        #     reverse=True
        # )
        sorted_dict_list = sorted(
            e_p_dict_list,
            key=lambda item: item['priority'],
            reverse=True
        )
        if sorted_dict_list:
            if sorted_dict_list[-1]['start_from'] != 0:
                sorted_dict_list[-1]['form'].add_error(
                    'start_from',
                    'First range must start from 0',
                )
            for index, item in enumerate(sorted_dict_list):
                if index == 0 and len(sorted_dict_list) > 1:

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


class TaxCalcSchemeInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(TaxCalcSchemeInlineFormSet, self).clean()
        e_p_dict_list = []
        for form in self.forms:
            instance = self.instance
            if form.cleaned_data:
                start_from = form.cleaned_data.get("start_from")
                end_to = form.cleaned_data.get("end_to")
                priority = form.cleaned_data.get("priority")
                DELETE = form.cleaned_data.get("DELETE")

                if end_to:
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
        if sorted_dict_list:
            if sorted_dict_list[-1]['start_from'] != 0:
                sorted_dict_list[-1]['form'].add_error(
                    'start_from',
                    'First range must start from 0'
                )
            for index, item in enumerate(sorted_dict_list):
                if index == 0:
                    if not instance.end_to:
                        if item['end_to'] is not None:
                            item['form'].add_error(
                                'end_to',
                                'Last range end to should be None'
                            )
                    else:
                        if item['end_to'] != instance.end_to:
                            item['form'].add_error(
                                'end_to',
                                'Last range end to should be equal to %d' % instance.end_to,
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

    def __init__(self, *args, **kwargs):
        super(AllowanceForm, self).__init__(*args, **kwargs)
        choices = [(obj.id, obj.__unicode__()) for obj in
                   sorted(EmployeeGrade.objects.all(), key=lambda m: m.__unicode__())]
        self.fields['employee_grade'].widget = Select(choices=choices)

    def clean(self):
        cleaned_data = super(AllowanceForm, self).clean()
        payment_cycle = cleaned_data.get("payment_cycle")
        year_payment_cycle_month = cleaned_data.get("year_payment_cycle_month")

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

        payment_cycle = cleaned_data.get("payment_cycle")
        year_payment_cycle_month = cleaned_data.get("year_payment_cycle_month")

        if payment_cycle == 'Y' and not year_payment_cycle_month:
            self.add_error(
                'year_payment_cycle_month',
                'This field is needed if it is a yearly allowance'
            )


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = '__all__'



    # def clean(self):
    #     cleaned_data = super(DeductionForm, self).clean()
    #
    #     deduction_for = cleaned_data.get("deduction_for")
    #     explicit_acc = cleaned_data.get("explicit_acc")
    #     in_acc_type = cleaned_data.get("in_acc_type")
    #
    #     if deduction_for == 'EXPLICIT ACC' and not explicit_acc:
    #         self.add_error(
    #             'explicit_acc',
    #             'This field is required with Deduction for Explicit Account'
    #         )
    #     elif deduction_for == 'EMPLOYEE ACC' and not in_acc_type:
    #         self.add_error(
    #             'in_acc_type',
    #             'This field is required with Deduction for Employee Account'
    #         )


class EmployeeForm(HTML5BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['optional_deductions'].queryset = DeductionName.objects.filter(is_optional=True)

    class Meta:
        model = Employee
        exclude = ('accounts', 'incentives')


class IncentiveNameForm(HTML5BootstrapModelForm):
    class Meta:
        model = IncentiveName
        fields = '__all__'


class AllowanceNameForm(HTML5BootstrapModelForm):
    class Meta:
        model = AllowanceName
        exclude = ('account_category',)


class MaritalStatusForm(HTML5BootstrapModelForm):
    class Meta:
        model = MaritalStatus
        fields = '__all__'


class TaxSchemeForm(HTML5BootstrapModelForm):
    class Meta:
        model = TaxScheme
        fields = '__all__'

        widgets = {
            'marital_status': Select(attrs={'readonly': "true"}),
            'start_from': NumberInput(attrs={'readonly': "true"}),
            'end_to': NumberInput(attrs={'readonly': "true"}),
            'priority': NumberInput(attrs={'readonly': "true"}),
        }


class ReportHrForm(HTML5BootstrapModelForm):
    class Meta:
        model = ReportHR
        fields = '__all__'



# These are crud formset
EmployeeIncentiveFormSet = forms.inlineformset_factory(
    Employee,
    Incentive,
    extra=1,
    fields='__all__',
    formset=IncentiveInlineFormset
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
    form=AllowanceForm,
    extra=1,
    exclude=('account',),
    formset=AllowanceInlineFormset
)

DeductionNameFormSet = forms.modelformset_factory(
    DeductionName,
    extra=1,
    can_delete=True,
    exclude=('deduct_in_category',),
)

EmployeeGradeFormSet = forms.modelformset_factory(
    EmployeeGrade,
    extra=1,
    can_delete=True,
    fields='__all__',
)

EmployeeGradeGroupFormSet = forms.modelformset_factory(
    EmployeeGradeGroup,
    extra=1,
    can_delete=True,
    fields='__all__',
)


class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)
        choices = [(obj.id, obj.__unicode__())  for obj in sorted(EmployeeGrade.objects.all(),  key=lambda m: m.__unicode__())]
        self.fields['grade'].widget = Select(choices=choices)

DesignationFormSet = forms.modelformset_factory(
    Designation,
    form=DesignationForm,
    extra=1,
    can_delete=True,
    fields='__all__',
)

IncentiveNameDetailFormSet = forms.modelformset_factory(
    IncentiveName,
    extra=1,
    can_delete=True,
    exclude=('account_category',),
)

TaxSchemeFormSet = forms.inlineformset_factory(
    MaritalStatus,
    TaxScheme,
    extra=1,
    fields='__all__',
    formset=TaxSchemeInlineFormSet
)

TaxCalcSchemeFormSet = forms.inlineformset_factory(
    TaxScheme,
    TaxCalcScheme,
    extra=1,
    fields='__all__',
    formset=TaxCalcSchemeInlineFormSet
)

ReportHrTableFormSet = forms.inlineformset_factory(
    ReportHR,
    ReportTable,
    extra=1,
    exclude=('account',),
    # formset=AllowanceInlineFormset
)