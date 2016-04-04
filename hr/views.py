from django.shortcuts import render
from .forms import PaymentRowForm, PayrollEntryForm, GroupPayrollForm
from .models import Employee
from django.http import HttpResponse, JsonResponse
from datetime import datetime


# Create your views here.
def payroll_entry(request):
    main_form = GroupPayrollForm(initial={'payroll_type': 'BRANCH'})
    row_form = PaymentRowForm()
    return render(request, 'payroll_entry.html', {'r_form': row_form, 'm_form': main_form})


# def group_payroll_branch(request):
#     form = GroupPayrollForm()
#     return render(request, 'group_payroll_branch.html', {'form': form})

def get_employee_account(request):
    error = {}
    if request.POST:
        employee_id = request.POST.get('paid_employee', None)
        if employee_id:
            employee = Employee.objects.get(id=int(employee_id))
        else:
            error['employee'] = 'No such employee'
        try:
            # Validate it for bsdate
            paid_from_date = datetime.strptime(request.POST.get('paid_from_date', None), '%Y-%m-%d')
        except:
            error['paid_from_date'] = 'Incorrect Date Format'
        try:
            paid_to_date = datetime.strptime(request.POST.get('paid_to_date', None), '%Y-%m-%d')
        except:
            error['paid_to_date'] = 'Incorrect Date Format'
        if error:
            return JsonResponse(error)
        # Now calculate all the values and give a good meaningful response
        employee_scale = employee.current_salary()
        total_work_day = paid_to_date - paid_from_date
        salary = employee_scale/30 * total_work_day

        # Now add allowence to the salary(salary = salary + allowence)
        # Question here is do we need to deduct from incentove(I gues not)
        for obj employee.allowence:
            if obj.incentive_cycle == 'Y':
                # Pay when we in within of dat month
                pass
            elif obj.incentive_cycle == 'M':
                pass
            elif obj.incentive_cycle == 'D':
                pass
            else:
                pass
        return HttpResponse(request.POST)
    else:
        return HttpResponse('Damn no request.POST')


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