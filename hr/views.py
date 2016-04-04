from django.shortcuts import render
from .forms import PaymentRowForm, PayrollEntryForm, GroupPayrollForm
from .models import Employee, Deduction
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
        current_salary = employee.current_salary()
        total_work_day = paid_to_date - paid_from_date
        salary = current_salary/30 * total_work_day

        # Now add allowence to the salary(salary = salary + allowence)
        # Question here is do we need to deduct from incentove(I gues not)
        for obj in employee.allowences:
            allowence = 0
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                pass
            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    allowence += obj.amount/30.0 * total_work_day
                else:
                    allowence += obj.rate/100.0 * salary
            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    allowence += obj.amount * total_work_day
                else:
                    # Does this mean percentage in daily wages
                    allowence += obj.rate/100.0 * salary
            else:
                # This is hourly case(Dont think we have it)
                pass

        salary += allowence

        # now calculate incentive if it has but not to add to salary just to transact seperately 
        for obj in employee.incentives:
            incentive = 0
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                pass
            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    incentive += obj.amount/30.0 * total_work_day
                else:
                    incentive += obj.rate/100.0 * salary
            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    incentive += obj.amount * total_work_day
                else:
                    # Does this mean percentage in daily wages
                    incentive += obj.rate/100.0 * salary
            else:
                # This is hourly case(Dont think we have it)
                pass

        # Now the deduction part from the salary
        deductions = sorted(Deduction.objects.all(), key=lambda obj: obj.priority)
        deduction = 0
        deduction_detail = {}
        for obj in deductions:
            if obj.deduction_for == 'EMPLOYEE ACC':
                if obj.account_type.name == 'SANCHAYA KOSH':
                    sanchaya_deduction = {}
                    sanchaya_deduction['amount'] = 0
                    if obj.deduct_type == 'AMOUNT':
                        sanchaya_deduction['amount'] += obj.amount/30.0 * total_work_day
                    else:
                        # Rate
                        sanchaya_deduction['amount'] += obj.rate/100.0 * salary
                    if employee.is_permanent:
                        sanchaya_deduction['amount'] *= 2
                    deduction_detail['sanchaya_deduction'] = sanchaya_deduction
                    deduction += sanchaya_deduction['amount']
                elif obj.account_type.name == 'NALA ACC':
                    nala_deduction = 0
                    if obj.deduct_type == 'AMOUNT':
                        nala_deduction += obj.amount/30.0 * total_work_day
                    else:
                        # Rate
                        nala_deduction += obj.rate/100.0 * salary
                    if employee.is_permanent:
                        nala_deduction *= 2
                    deduction_detail['nala_deduction'] = nala_deduction
                    deduction += nala_deduction
                elif obj.account_type.name == 'INSURANCE ACC':
                    pass
                elif obj.account_type.name == 'BANK ACC':
                    pass
            else:
                # EXPLICIT ACC
                pass


        return HttpResponse('Well we are doing just fine')

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