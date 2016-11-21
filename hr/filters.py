import django_filters
from mptt.forms import TreeNodeChoiceField

from hr.models import Employee, PayrollEntry, BranchOffice, PayrollConfig


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
            self.form.fields['working_branch'].queryset = BranchOffice.objects.filter(id=accountant_branch_id)
        self.form.fields['working_branch'].empty_label = None

    is_active = django_filters.BooleanFilter(help_text='')

    working_branch = TreeNodeModelChoiceFilter(
        queryset=BranchOffice.objects.all(),
        help_text='',
    )

    class Meta:
        model = Employee
        fields = ['is_active', 'working_branch']


# class PayrollEntryFilter(django_filters.FilterSet):
#     class Meta:
#         model = PayrollEntry
#         fields = ['']
