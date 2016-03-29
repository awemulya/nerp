from django.shortcuts import render
from .forms import PaymentRowForm, PayrollEntryForm
from .models import Employee


# Create your views here.
def payroll_entry(request):
    form = PaymentRowForm()
    return render(request, 'payroll_entry.html', {'form': form})


def calculate_salry(request):
    data = {}
    data['allowence'] = 0
    data['incentive'] = 0
    data['deduced'] = 0
    if request.POST:
        employee_id = request.POST.get('employee', None)
        pay_from = request.POST.get('paid_from_date', None)
        pay_to = request.POST.get('paid_to_date', None)

        employee = Employee.objects.get(id=employee_id)
        salary = employee.current_salary()
        # Now datao sanchai kosh
        if employee.is_permanent:
            sanchaya_deduction = 20/100 * salary
            #Transact sanchaya deduction to sanchaya kosh employee account
            salary = salary = sanchaya_deduction
        else:
            sanchaya_deduction = 10/100 * salary
            #Transact sanchaya deduction to sanchaya kosh employee account
            salary = salary = sanchaya_deduction

        # Transact Rs. 200 to Nagarik Lagani Kosh
        salary = salary - 200
        



        # Now generate salary and dont transact here,
        # Trancsaction should be done when the row is saved 