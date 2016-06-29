from app.utils.forms import KOModelForm, HTML5BootstrapModelForm
from core.models import Employee, Donor, BudgetHead


class EmployeeForm(KOModelForm):
    class Meta:
        model = Employee
        exclude = ['account']


class DonorForm(HTML5BootstrapModelForm):
    class Meta:
        model = Donor
        fields = ('name',)


class BudgetHeadForm(HTML5BootstrapModelForm):
    class Meta:
        model = BudgetHead
        fields = '__all__'
