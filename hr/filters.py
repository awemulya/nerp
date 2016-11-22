import django_filters
from mptt.forms import TreeNodeChoiceField

from hr.models import Employee, PayrollEntry, BranchOffice, PayrollConfig
from hr.filter_forms import EmployeeFilterForm, PayrollEntryFilterForm


class TreeNodeModelChoiceFilter(django_filters.Filter):
    field_class = TreeNodeChoiceField


class EmployeeFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(EmployeeFilter, self).__init__(*args, **kwargs)

        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.form.fields['working_branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.form.fields['working_branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)
        self.form.fields['working_branch'].empty_label = None

    is_active = django_filters.BooleanFilter(help_text='')

    working_branch = TreeNodeModelChoiceFilter(
        queryset=BranchOffice.objects.all(),
        help_text='',
    )

    class Meta:
        model = Employee
        # form = EmployeeFilterForm
        fields = {
            'is_active': ['exact'],
            'working_branch': ['exact']
        }


class PayrollEntryFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        accountant_branch_id = kwargs.pop('accountant_branch_id')
        super(PayrollEntryFilter, self).__init__(*args, **kwargs)

        if PayrollConfig.get_solo().parent_can_generate_payroll:
            self.form.fields['branch'].queryset = BranchOffice.objects.get(
                id=accountant_branch_id).get_descendants(include_self=True)
        else:
            self.form.fields['branch'].queryset = BranchOffice.objects.filter(
                id=accountant_branch_id)
        self.form.fields['branch'].empty_label = None

    # is_active = django_filters.BooleanFilter(help_text='')
    #
    # branch = TreeNodeModelChoiceFilter(
    #     queryset=BranchOffice.objects.all(),
    #     help_text='',
    # )

    class Meta:
        model = PayrollEntry
        form = PayrollEntryFilterForm
        fields = {
            'branch': ['exact'],
            'paid_from_date': ['exact'],
            'paid_to_date': ['exact', 'lte'],
        }
