from django.shortcuts import render
from .forms import PaymentRowForm, PayrollEntryForm, GroupPayrollForm
from .models import Employee, Deduction, EmployeeAccount, IncomeTaxRate
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from njango.nepdate import bs2ad
from .models import get_y_m_tuple_list
from .bsdate import BSDate
import pdb


CALENDER = 'BS'
F_INCOME_TAX_DISCOUNT_RATE = 10


def bs_date2tuple(date_string):
    as_list = date_string.split('-')
    date_tuple = (
        int(as_list[0]),
        int(as_list[1]),
        int(as_list[2])
        )
    # If possible varify this
    return date_tuple


def get_account_id(employee_object, account_type):
    return EmployeeAccount.objects.get(
        employee=employee_object,
        account_type__name=account_type
    ).account.id


def delta_month_date(p_from, p_to):
    y_m_tuple = get_y_m_tuple_list(p_from, p_to)
    total_month = len(y_m_tuple)
    if type(p_from) == type(p_to):
        total_work_day = (p_to - p_from).days


    # Need to test this (this can be made a function)
    # if p_from.year == p_to.year:
    #     total_month += p_from.month - p_to.month + 1
    #     for ob in range(p_from.month, p_to.month + 1):
    #         total_work_day += bs[p_from.year][ob-1]
    # else:
    #     while p_from <= p_to:
    #         total_work_day += bs[p_from.year][p_from.month-1]
    #         if p_from.month < 12:
    #             p_from = date(p_from.year, p_from.month+1, p_from.day)
    #             total_month += 1
    #         else:
    #             p_from = date(p_from.year + 1, 1, p_from.day)
    #             total_month += 1
    return (total_month, total_work_day)


# Create your views here.
def payroll_entry(request):
    main_form = GroupPayrollForm(initial={'payroll_type': 'BRANCH'})
    row_form = PaymentRowForm()
    return render(
        request,
        'payroll_entry.html',
        {
          'r_form': row_form,
          'm_form': main_form
        })


# def group_payroll_branch(request):
#     form = GroupPayrollForm()
#     return render(request, 'group_payroll_branch.html', {'form': form})

def get_employee_account(request):
    error = {}
    result_data = {}
    result_data['respone'] = []
    employee_response = {}
    if request.POST:
        employee_id = request.POST.get('paid_employee', None)
        if employee_id:
            employee = Employee.objects.get(id=int(employee_id))
            employee_response['employee_id'] = employee.id
        else:
            error['employee'] = 'No such employee'

        if CALENDER == 'AD':
            try:
                # Validate it for bsdate
                paid_from_date = datetime.strptime(
                    request.POST.get('paid_from_date', None), '%Y-%m-%d').date()
            except:
                error['paid_from_date'] = 'Incorrect Date Format'
            try:
                paid_to_date = datetime.strptime(
                    request.POST.get('paid_to_date', None), '%Y-%m-%d').date()
            except:
                error['paid_to_date'] = 'Incorrect Date Format'
        else:
            try:
                paid_from_date = BSDate(bs_date2tuple(
                    request.POST.get('paid_from_date', None), '%Y-%m-%d'
                    ))
            except:
                error['paid_from_date'] = 'Incorrect BS Date'
            try:
                paid_to_date = BSDate(bs_date2tuple(
                    request.POST.get('paid_to_date', None), '%Y-%m-%d'
                    ))
            except:
                error['paid_from_date'] = 'Incorrect BS Date'

        if paid_to_date < paid_from_date:
                error['invalid_date_range'] = 'Date: paid to must be greater than paid from'

        if error:
            return JsonResponse(error)
        # Now calculate all the values and give a good meaningful response
        # total_work_day = paid_to_date - paid_from_date
        total_month, total_work_day = delta_month_date(
                                                       paid_from_date,
                                                       paid_to_date
                                                       )
        # total_work_day = 0
        # total_month = 0

        # Need to test this (this can be made a function)
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

        salary = employee.current_salary_by_month(
            paid_from_date,
            paid_to_date
            )

        # total_month = paid_to_date.month - paid_from_date.month + 1

        # if paid_from_date == paid_to_date:
        #     salary = current_salary()
        # else:
        #     salary = current_salary(total_month - 1)

        # Now add allowence to the salary(salary = salary + allowence)
        # Question here is do we need to deduct from incentove(I gues not)
        for obj in employee.allowences.all():
            allowence = 0
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                pass
            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    allowence += obj.amount * total_month
                else:
                    allowence += obj.amount_rate / 100.0 * salary
            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    allowence += obj.amount * total_work_day
                else:
                    # Does this mean percentage in daily wages
                    allowence += obj.amount_rate / 100.0 * salary
            else:
                # This is hourly case(Dont think we have it)
                pass

        employee_response['allowence'] = allowence
        salary += allowence
        # employee_response['salay_allowence_included'] = salary

        # now calculate incentive if it has but not to add to salary just to
        # transact seperately
        for obj in employee.incentives.all():
            incentive = 0
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                pass
            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    incentive += obj.amount * total_month
                else:
                    incentive += obj.amount_rate / 100.0 * salary
            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    incentive += obj.amount * total_work_day
                else:
                    # Does this mean percentage in daily wages
                    incentive += obj.amount_rate / 100.0 * salary
            else:
                # This is hourly case(Dont think we have it)
                pass

        employee_response['incentive'] = incentive
        salary += incentive

        # Now the deduction part from the salary
        deductions = sorted(
            Deduction.objects.all(), key=lambda obj: obj.priority)
        deduction = 0
        deduction_detail = {}
        for obj in deductions:
            if obj.deduction_for == 'EMPLOYEE ACC':
                deduction_detail[obj.in_acc_type.name] = {}
                deduction_detail[obj.in_acc_type.name]['amount'] = 0
                if obj.deduct_type == 'AMOUNT':
                    deduction_detail[obj.in_acc_type.name][
                        'amount'] += obj.amount / 30.0 * total_work_day
                else:
                    # Rate
                    deduction_detail[obj.in_acc_type.name][
                        'amount'] += obj.amount_rate / 100.0 * salary
                if employee.is_permanent:
                    if obj.in_acc_type.permanent_multiply_rate:
                        deduction_detail[obj.in_acc_type.name][
                          'amount'] *= obj.in_acc_type.permanent_multiply_rate
                deduction_detail[obj.in_acc_type.name][
                    'account_id'] = get_account_id(
                        employee,
                        obj.in_acc_type.name
                        )
                deduction += deduction_detail[obj.in_acc_type.name]['amount']

            else:
                name = '_'.join(obj.name.split(' ')).lower()
                deduction_detail['others'] = {}
                deduction_detail['others'][name] = {}
                deduction_detail['others'][name]['amount'] = 0
                # EXPLICIT ACC
                if obj.deduct_type == 'AMOUNT':
                    deduction_detail['others'][name][
                        'amount'] += obj.amount / 30.0 * total_work_day
                else:
                    # Rate
                    deduction_detail['others'][name][
                        'amount'] += obj.amount_rate / 100.0 * salary
                deduction_detail['others'][name][
                    'account_id'] = obj.explicit_acc.id
                deduction += deduction_detail['others'][name]['amount']

        # Income tax logic
        income_tax = 0
        for obj in IncomeTaxRate.objects.all():
            if obj.is_last:
                if salary >= obj.start_from:
                    income_tax = obj.tax_rate/100 * salary
                    if obj.rate_over_tax_amount:
                        income_tax += obj.rate_over_tax_amount/100 * income_tax
            else:
                if salary >= obj.start_from and salary <= obj.end_to:
                    income_tax = obj.tax_rate/100 * salary
                    if obj.rate_over_tax_amount:
                        income_tax += obj.rate_over_tax_amount/100 * income_tax
            if employee.sex == 'F':
                income_tax -= F_INCOME_TAX_DISCOUNT_RATE/100 * income_tax

        employee_response['income_tax'] = income_tax
        employee_response['deduced_amount'] = deduction
        employee_response['paid_amount'] = salary - deduction - income_tax
        employee_response['deduction_detail'] = deduction_detail

        return JsonResponse(employee_response)

    else:
        return HttpResponse('Damn no request.POST')


def test(request):
    emp = Employee.objects.get(id=1)
    x = date(2072, 2, 1)
    y = date(2072, 4, 25)

    salary = emp.current_salary_by_day('BS', x, y)
    salary1 = emp.current_salary_by_month('BS', x, y)
    pdb.set_trace()

    return HttpResponse(salary)
# def calculate_salry(request):
#     data = {}
#     data['allowence'] = 0
#     data['incentive'] = 0
#     data['deduced'] = 0
#     if request.POST:
#         employee_id = request.POST.get('employee', None)
#         pay_from = request.POST.get('paid_from_date', None)
#         pay_to = request.POST.get('paid_to_date', None)

#         employee = Employee.objects.get(id=employee_id)
#         salary = employee.current_salary()
#         # Now datao sanchai kosh
#         if employee.is_permanent:
#             sanchaya_deduction = 20 / 100 * salary
#             # Transact sanchaya deduction to sanchaya kosh employee account
#             salary = salary = sanchaya_deduction
#         else:
#             sanchaya_deduction = 10 / 100 * salary
#             # Transact sanchaya deduction to sanchaya kosh employee account
#             salary = salary = sanchaya_deduction

#         # Transact Rs. 200 to Nagarik Lagani Kosh
#         salary = salary - 200

#         # Now generate salary and dont transact here,
#         # Trancsaction should be done when the row is saved
