import django_filters
from hr.models import Employee, PayrollEntry, BranchOffice


class EmployeeFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(help_text='')
    working_branch = django_filters.ModelChoiceFilter(
        queryset=BranchOffice.objects.all(),
        help_text=''
    )

    class Meta:
        model = Employee
        fields = ['is_active', 'working_branch']


# class PayrollEntryFilter(django_filters.FilterSet):
#     class Meta:
#         model = PayrollEntry
#         fields = ['']
