from django.shortcuts import render
from .forms import PaymentRowForm, PayrollEntryForm, GroupPayrollForm
from .models import Employee, Deduction
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime
from njango.nepdate import bs


def delta_month_date(p_from, p_to):
    total_work_day = 0
    total_month = 0

    # Need to test this (this can be made a function)
    if p_from.year == p_to.year:
        total_month += p_from.month - p_to.month + 1
        for ob in range(p_from.month, p_to.month + 1):
            total_work_day += bs[p_from.year][ob-1]
    else:
        while p_from <= p_to:
            total_work_day += bs[p_from.year][p_from.month-1]
            if p_from.month < 12:
                p_from = date(p_from.year, p_from.month+1, p_from.day)
                total_month += 1
            else:
                p_from = date(p_from.year + 1, 1, p_from.day)
                total_month += 1
    return (total_month, total_work_day)


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
        # total_work_day = paid_to_date - paid_from_date
        total_month, total_work_day = delta_month_date(paid_from_date,
                                                       paid_to_date)
        # total_work_day = 0
        # total_month = 0

        # # Need to test this (this can be made a function)
        # if paid_from_date.year == paid_to_date.year:
        #     total_month += paid_from_date.month - paid_to_date.month + 1
        #     for ob in range(paid_from_date.month, paid_to_date.month + 1):
        #         total_work_day += bs[paid_from_date.year][ob-1]
        # else:
        #     p_from = paid_from_date
        #     p_to = paid_to_date

        #     while p_from <= p_to:
        #         total_work_day += bs[p_from.year][p_from.month-1]
        #         if p_from.month < 12:
        #             p_from = date(p_from.year, p_from.month+1, p_from.day)
        #             total_month += 1
        #         else:
        #             p_from = date(p_from.year + 1, 1, p_from.day)
        #             total_month += 1

        salary = employee.current_salary(total_month-1)

        # total_month = paid_to_date.month - paid_from_date.month + 1

        # if paid_from_date == paid_to_date:
        #     salary = current_salary()
        # else:
        #     salary = current_salary(total_month - 1)

        # Now add allowence to the salary(salary = salary + allowence)
        # Question here is do we need to deduct from incentove(I gues not)
        for obj in employee.allowences:
            allowence = 0
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                pass
            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    allowence += obj.amount * total_month
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
                    incentive += obj.amount * total_month
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
                deduction_detail[obj.in_acc_type.name] = {}
                deduction_detail[obj.in_acc_type.name]['amount'] = 0
                if obj.deduct_type == 'AMOUNT':
                    deduction_detail[obj.in_acc_type.name]['amount'] += obj.amount/30.0 * total_work_day
                else:
                    # Rate
                    deduction_detail[obj.in_acc_type.name]['amount'] += obj.rate/100.0 * salary
                if employee.is_permanent:
                    if obj.in_acc_type.permanent_multiply_rate:
                        deduction_detail[obj.in_acc_type.name]['amount'] *= obj.in_acc_type.permanent_multiply_rate
                deduction_detail[obj.in_acc_type.name]['account_id'] = getattr(employee, obj.in_acc_type.name).id
                deduction += deduction_detail[obj.in_acc_type.name]['amount']

            else:
                name = '_'.join(obj.name.split(' ')).lower()
                deduction_detail['others'] = {}
                deduction_detail['others'][name] = {}
                deduction_detail['others'][name]['amount'] = 0
                # EXPLICIT ACC
                if obj.deduct_type == 'AMOUNT':
                    deduction_detail['others'][name]['amount'] += obj.amount/30.0 * total_work_day
                else:
                    # Rate
                    deduction_detail['others'][name]['amount'] += obj.rate/100.0 * salary
                deduction_detail['others'][name]['account_id'] = obj.explicit_acc.id
                deduction += deduction_detail['others'][name]['amount']



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