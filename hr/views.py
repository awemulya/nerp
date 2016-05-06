from __future__ import division
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from .forms import GroupPayrollForm, PaymentRowFormSet, DeductionFormSet, IncentiveFormSet, AllowanceFormSet, get_deduction_names, get_incentive_names, get_allowance_names
from .models import Employee, Deduction, EmployeeAccount, IncomeTaxRate, ProTempore, IncentiveName, AllowanceName, DeductionDetail, AllowanceDetail, IncentiveDetail, PaymentRecord, PayrollEntry
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from calendar import monthrange as mr
from njango.nepdate import bs
from .models import get_y_m_tuple_list
from .bsdate import BSDate
from .helpers import are_side_months, bs_str2tuple, get_account_id, delta_month_date, delta_month_date_impure, emp_salary_eligibility, month_cnt_inrange
import pdb


CALENDAR = 'BS'
F_INCOME_TAX_DISCOUNT_RATE = 10


def verify_request_date(request):
    error = {}
    paid_from_date = None
    paid_to_date = None
    if request.POST:
        if CALENDAR == 'AD':
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

                paid_from_date = BSDate(*bs_str2tuple(
                    request.POST.get('paid_from_date', None)
                ))

            except:
                error['paid_from_date'] = 'Incorrect BS Date'
            try:
                paid_to_date = BSDate(*bs_str2tuple(
                    request.POST.get('paid_to_date', None)
                ))
            except:
                error['paid_to_date'] = 'Incorrect BS Date'

        if paid_to_date and paid_from_date:
            if paid_to_date < paid_from_date:
                error['invalid_date_range'] = \
                    'Date: paid to must be greater than paid from'

        if error:
            return error
        else:
            monthly_payroll = request.POST.get(
                'monthly_payroll',
                None
            )
            if monthly_payroll == u'true':
                if isinstance(paid_from_date, date):
                    to_month_days = mr(
                        paid_to_date.year,
                        paid_to_date.month
                    )[1]
                    paid_from_date = date(
                        paid_from_date.year,
                        paid_from_date.month,
                        1
                    )
                    paid_to_date = date(
                        paid_to_date.year,
                        paid_to_date.month,
                        to_month_days
                    )

                else:
                    to_month_days = bs[
                        paid_to_date.year][
                        paid_to_date.month - 1
                    ]
                    paid_from_date = BSDate(
                        paid_from_date.year,
                        paid_from_date.month,
                        1
                    )
                    paid_to_date = BSDate(
                        paid_to_date.year,
                        paid_to_date.month,
                        to_month_days
                    )
            return paid_from_date, paid_to_date


# def get_underscore_formset(string):
#     # pdb.set_trace()

#     html_tree = html.fragment_fromstring(string, create_parent='tr')
#     for branch in html_tree:
#         for s_branch in branch:
#             if s_branch.tag == 'th':
#                 s_branch.drop_tree()
#             elif s_branch.tag == 'td':
#                 for ele in s_branch:
#                     input_id = ele.get('id')
#                     input_id_m = [o if o != '0' else '${$index}' for o in input_id.split('-')]
#                     ele.set('id', '-'.join(input_id_m))

#                     input_name = ele.get('name')
#                     input_name_m = [o if o != '0' else '${$index}' for o in input_name.split('-')]
#                     ele.set('id', '-'.join(input_name_m))
#                     # pdb.set_trace()
#         if branch.tag == 'tr':
#             branch.drop_tag()
#             # pdb.set_trace()
#     return html.tostring(html_tree)


def salary_deduction_unit():
    pass


def salary_taxation_unit():
    pass


def salary_detail_impure_months(employee, paid_from_date, paid_to_date):
    employee_response = {}
    employee_response['paid_employee'] = employee.id
    employee_response['employee_grade'] = employee.designation.grade.grade_name
    employee_response['employee_designation'] = employee.designation.designation_name
    # Watchout
    total_month, total_work_day = delta_month_date_impure(
        paid_from_date,
        paid_to_date
    )
    # watchout

    salary = employee.current_salary_by_day(
        paid_from_date,
        paid_to_date
    )

    # Now add allowance to the salary(salary = salary + allowance)
    # Question here is do we need to deduct from incentove(I gues not)
    allowance = 0
    for obj in employee.allowances.all():
        if obj.payment_cycle == 'Y':
            # check obj.year_payment_cycle_month to add to salary
            pass
        elif obj.payment_cycle == 'M':
            if obj.sum_type == 'AMOUNT':
                allowance += obj.amount * total_month
            else:
                allowance += obj.amount_rate / 100.0 * salary
        elif obj.payment_cycle == 'D':
            if obj.sum_type == 'AMOUNT':
                allowance += obj.amount * total_work_day
            else:
                # Does this mean percentage in daily wages
                allowance += obj.amount_rate / 100.0 * salary
        else:
            # This is hourly case(Dont think we have it)
            pass

    employee_response['allowance'] = allowance
    salary += allowance

    # now calculate incentive if it has but not to add to salary just to
    # transact seperately
    incentive = 0
    for obj in employee.incentives.all():
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
    # salary += incentive

    # Now the deduction part from the salary
    deductions = sorted(
        Deduction.objects.all(), key=lambda obj: obj.priority)

    # Addition of PF and bima to salary if employee is permanent
    for item in deductions:
        if employee.is_permanent:
            if item.add2_init_salary and item.deduction_for == 'EMPLOYEE ACC':
                if item.deduct_type == 'AMOUNT':
                    salary += item.amount * total_month
                else:
                    # Rate
                    salary += item.amount_rate / 100.0 * salary

    deduction = 0
    # deduction_detail = []
    for obj in deductions:
        # deduction_detail_object = {}
        if obj.deduction_for == 'EMPLOYEE ACC':
            employee_response['%s_%s' % (obj.in_acc_type.name, obj.id)] = 0

            if (employee.is_permanent or obj.with_temporary_employee) and employee.has_account(obj.in_acc_type):

                if obj.deduct_type == 'AMOUNT':
                    employee_response['%s_%s' % (obj.in_acc_type.name, obj.id)] += obj.amount * total_month
                else:
                    # Rate
                    # deduction_detail_object['amount'] += obj.amount_rate / 100.0 * salary
                    employee_response['%s_%s' % (obj.in_acc_type.name, obj.id)] += obj.amount_rate / 100.0 * salary

                if employee.is_permanent:
                    if obj.in_acc_type.permanent_multiply_rate:
                        # deduction_detail_object['amount'] *= obj.in_acc_type.permanent_multiply_rate
                        employee_response['%s_%s' % (obj.in_acc_type.name, obj.id)] *= obj.in_acc_type.permanent_multiply_rate                 
                # deduction += deduction_detail_object['amount']
                deduction += employee_response['%s_%s' % (obj.in_acc_type.name, obj.id)]

        else:
            name = '_'.join(obj.name.split(' ')).lower()
            employee_response['%s_%s' % (name, obj.id)] = 0

            # EXPLICIT ACC
            if obj.deduct_type == 'AMOUNT':
                # deduction_detail_object[
                #     'amount'] += obj.amount * total_month
                employee_response['%s_%s' % (name, obj.id)] += obj.amount * total_month
            else:
                employee_response['%s_%s' % (name, obj.id)] += obj.amount_rate / 100.0 * salary
            deduction += employee_response['%s_%s' % (name, obj.id)]

    # Income tax logic
    income_tax = 0
    for obj in IncomeTaxRate.objects.all():
        if obj.is_last:
            if salary >= obj.start_from:
                income_tax = obj.tax_rate / 100 * salary
                if obj.rate_over_tax_amount:
                    income_tax += obj.rate_over_tax_amount / 100 * income_tax
        else:
            if salary >= obj.start_from and salary <= obj.end_to:
                income_tax = obj.tax_rate / 100 * salary
                if obj.rate_over_tax_amount:
                    income_tax += obj.rate_over_tax_amount / 100 * income_tax
        if employee.sex == 'F':
            income_tax -= F_INCOME_TAX_DISCOUNT_RATE / 100 * income_tax

    employee_response['income_tax'] = income_tax
    employee_response['deduced_amount'] = deduction
    # employee_response['deduction_detail'] = deduction_detail
    # employee_response['other_deduction'] = other_deduction

    # Handle Pro Tempore
    # paid flag should be set after transaction
    pro_tempores = ProTempore.objects.filter(employee=employee)
    p_t_amount = 0
    to_be_paid_pt_ids = []
    for p_t in pro_tempores:
        if not p_t.paid:
            if isinstance(p_t.appoint_date, date):
                p_t_amount += p_t.pro_tempore.current_salary_by_day(
                    p_t.appoint_date,
                    p_t.dismiss_date
                )

                to_be_paid_pt_ids.append(p_t.id)
            else:
                p_t_amount += p_t.pro_tempore.current_salary_by_day(
                    BSDate(*bs_str2tuple(p_t.appoint_date)),
                    BSDate(*bs_str2tuple(p_t.dismiss_date))
                )
                to_be_paid_pt_ids.append(p_t.id)

    employee_response['pro_tempore_amount'] = p_t_amount
    employee_response['pro_tempore_ids'] = to_be_paid_pt_ids
    # First allowence added to salary for deduction and income tax.
    # For pure salary here added allowance should be duduced
    employee_response['salary'] = salary - allowance
    employee_response['employee_bank_account_id'] = get_account_id(
        employee, 'bank_account')

    employee_response['paid_amount'] = salary - deduction - income_tax +\
        p_t_amount + incentive

    return employee_response


def get_employee_salary_detail(employee, paid_from_date, paid_to_date):
    row_errors = []
    eligible, error = emp_salary_eligibility(
        employee,
        paid_from_date,
        paid_to_date
    )
    if not eligible:
        row_errors.append(error)
    employee_response = {}
    employee_response['paid_employee'] = employee.id
    employee_response['employee_grade'] = employee.designation.grade.grade_name
    employee_response['employee_designation'] = employee.designation.designation_name

    # This should be in if when we combine both monthly and daily payroll
    total_month, total_work_day = delta_month_date_impure(
        paid_from_date,
        paid_to_date
    )

    salary = employee.current_salary_by_day(
        paid_from_date,
        paid_to_date
    )

    # Now add allowance to the salary(salary = salary + allowance)
    # Question here is do we need to deduct from incentove(I gues not)
    allowance = 0
    # for obj in employee.allowances.all():
    for _name in AllowanceName.objects.all():
        # name = '_'.join(_name.name.split(' ')).lower()
        if _name in employee.allowances.all():
            obj = _name.allowances.all().filter(employee_grade=employee.designation.grade)
            if obj:
                obj = obj[0]
                if obj.payment_cycle == 'Y':
                    # check obj.year_payment_cycle_month to add to salary
                    cnt = month_cnt_inrange(
                        obj.year_payment_cycle_month,
                        paid_from_date,
                        paid_to_date
                    )
                    if cnt:
                        if obj.sum_type == 'AMOUNT':
                            employee_response['allowance_%d' % (_name.id)] = obj.amount * cnt
                            allowance += obj.amount * cnt
                        else:
                            employee_response['allowance_%d' % (_name.id)] = 0
                            # allowance += obj.amount_rate / 100.0 * salary
                    else:
                        employee_response['allowance_%d' % (_name.id)] = 0

                elif obj.payment_cycle == 'M':
                    if obj.sum_type == 'AMOUNT':
                        employee_response['allowance_%d' % (_name.id)] = obj.amount * total_month
                        allowance += obj.amount * total_month
                    else:
                        employee_response['allowance_%d' % (_name.id)] = obj.amount_rate / 100.0 * salary
                        allowance += obj.amount_rate / 100.0 * salary
                elif obj.payment_cycle == 'D':
                    if obj.sum_type == 'AMOUNT':
                        employee_response['allowance_%d' % (_name.id)] = obj.amount * total_work_day
                        allowance += obj.amount * total_work_day
                    else:
                        # Does this mean percentage in daily wages
                        employee_response['allowance_%d' % (_name.id)] = obj.amount_rate / 100.0 * salary
                        allowance += obj.amount_rate / 100.0 * salary
                # else:
                #     # This is hourly case(Dont think we have it)
                #     pass
            else:
                # Here also same as below
                employee_response['allowance_%d' % (_name.id)] = 0
        else:
            # give the parameters with empty value
            employee_response['allowance_%d' % (_name.id)] = 0

    employee_response['allowance'] = allowance
    salary += allowance

    # now calculate incentive if it has but not to add to salary just to
    # transact seperately
    incentive = 0
    # for obj in employee.incentives.all():
    for _name in IncentiveName.objects.all():
        # name = '_'.join(obj.name.split(' ')).lower()
        if _name in employee.incentives.all():
            obj = _name.incentives.all().filter(employee_grade=employee.designation.grade)
            if obj:
                obj = obj[0]
                # pdb.set_trace()
                if obj.payment_cycle == 'Y':
                    # check obj.year_payment_cycle_month to add to salary
                    cnt = month_cnt_inrange(
                        obj.year_payment_cycle_month,
                        paid_from_date,
                        paid_to_date
                    )
                    if cnt:
                        if obj.sum_type == 'AMOUNT':
                            employee_response['incentive_%d' % (_name.id)] = obj.amount * cnt
                            incentive += obj.amount * cnt
                        else:
                            employee_response['incentive_%d' % (_name.id)] = 0
                    else:
                        employee_response['incentive_%d' % (_name.id)] = 0

                elif obj.payment_cycle == 'M':
                    if obj.sum_type == 'AMOUNT':
                        employee_response['incentive_%d' % (_name.id)] = obj.amount * total_month
                        incentive += obj.amount * total_month
                    else:
                        employee_response['incentive_%d' % (_name.id)] = obj.amount_rate / 100.0 * salary
                        incentive += obj.amount_rate / 100.0 * salary
                elif obj.payment_cycle == 'D':
                    if obj.sum_type == 'AMOUNT':
                        employee_response['incentive_%d' % (_name.id)] = obj.amount * total_work_day
                        incentive += obj.amount * total_work_day
                    else:
                        # Does this mean percentage in daily wages
                        employee_response['incentive_%d' % (_name.id)] = obj.amount_rate / 100.0 * salary
                        incentive += obj.amount_rate / 100.0 * salary
                else:
                    # This is hourly case(Dont think we have it)
                    employee_response['incentive_%d' % (_name.id)] = 0
                    pass
            else:
                employee_response['incentive_%d' % (_name.id)] = 0
        else:
            employee_response['incentive_%d' % (_name.id)] = 0

    employee_response['incentive'] = incentive
    # salary += incentive

    # Now the deduction part from the salary
    deductions = sorted(
        Deduction.objects.all(), key=lambda obj: obj.priority)

    # Addition of PF and bima to salary if employee is permanent
    for item in deductions:
        if employee.is_permanent:
            if item.add2_init_salary and item.deduction_for == 'EMPLOYEE ACC':
                if item.deduct_type == 'AMOUNT':
                    salary += item.amount * total_month
                else:
                    # Rate
                    salary += item.amount_rate / 100.0 * salary

    deduction = 0
    # deduction_detail = []
    for obj in deductions:
        # deduction_detail_object = {}
        if obj.deduction_for == 'EMPLOYEE ACC':
            # name = '_'.join(obj.in_acc_type.name.split(' ')).lower
            employee_response['deduction_%d' % (obj.id)] = 0

            if (employee.is_permanent or obj.with_temporary_employee) and employee.has_account(obj.in_acc_type):

                if obj.deduct_type == 'AMOUNT':
                    employee_response['deduction_%d' % (obj.id)] += obj.amount * total_month
                else:
                    # Rate
                    # deduction_detail_object['amount'] += obj.amount_rate / 100.0 * salary
                    employee_response['deduction_%d' % (obj.id)] += obj.amount_rate / 100.0 * salary

                if employee.is_permanent:
                    if obj.in_acc_type.permanent_multiply_rate:
                        # deduction_detail_object['amount'] *= obj.in_acc_type.permanent_multiply_rate
                        employee_response['deduction_%d' % (obj.id)] *= obj.in_acc_type.permanent_multiply_rate                 
                # deduction += deduction_detail_object['amount']
                deduction += employee_response['deduction_%d' % (obj.id)]

        else:
            # name = '_'.join(obj.name.split(' ')).lower()
            employee_response['deduction_%d' % (obj.id)] = 0

            # EXPLICIT ACC
            if obj.deduct_type == 'AMOUNT':
                # deduction_detail_object[
                #     'amount'] += obj.amount * total_month
                employee_response['deduction_%d' % (obj.id)] += obj.amount * total_month
            else:
                employee_response['deduction_%d' % (obj.id)] += obj.amount_rate / 100.0 * salary
            deduction += employee_response['deduction_%d' % (obj.id)]

    # Income tax logic
    income_tax = 0
    for obj in IncomeTaxRate.objects.all():
        if obj.is_last:
            if salary >= obj.start_from:
                income_tax = obj.tax_rate / 100 * salary
                if obj.rate_over_tax_amount:
                    income_tax += obj.rate_over_tax_amount / 100 * income_tax
        else:
            if salary >= obj.start_from and salary <= obj.end_to:
                income_tax = obj.tax_rate / 100 * salary
                if obj.rate_over_tax_amount:
                    income_tax += obj.rate_over_tax_amount / 100 * income_tax
        if employee.sex == 'F':
            income_tax -= F_INCOME_TAX_DISCOUNT_RATE / 100 * income_tax

    employee_response['income_tax'] = income_tax
    employee_response['deduced_amount'] = deduction
    # employee_response['deduction_detail'] = deduction_detail
    # employee_response['other_deduction'] = other_deduction

    # Handle Pro Tempore
    # paid flag should be set after transaction
    pro_tempores = ProTempore.objects.filter(employee=employee)
    p_t_amount = 0
    to_be_paid_pt_ids = []
    for p_t in pro_tempores:
        if not p_t.paid:
            if isinstance(p_t.appoint_date, date):
                p_t_amount += p_t.pro_tempore.current_salary_by_day(
                    p_t.appoint_date,
                    p_t.dismiss_date
                )

                to_be_paid_pt_ids.append(p_t.id)
            else:
                p_t_amount += p_t.pro_tempore.current_salary_by_day(
                    BSDate(*bs_str2tuple(p_t.appoint_date)),
                    BSDate(*bs_str2tuple(p_t.dismiss_date))
                )
                to_be_paid_pt_ids.append(p_t.id)

    employee_response['pro_tempore_amount'] = p_t_amount
    employee_response['pro_tempore_ids'] = to_be_paid_pt_ids
    # First allowence added to salary for deduction and income tax.
    # For pure salary here added allowance should be duduced
    employee_response['salary'] = salary - allowance
    employee_response['employee_bank_account_id'] = get_account_id(
        employee, 'bank_account')

    employee_response['paid_amount'] = salary - deduction - income_tax +\
        p_t_amount + incentive

    if row_errors:
        for item in employee_response:
            if item not in ('paid_employee', 'employee_grade', 'employee_designation'):
                employee_response[item] = 0
        employee_response['row_errors'] = row_errors

    if isinstance(paid_from_date, date):
        employee_response['paid_from_date'] = '{:%Y-%m-%d}'.format(paid_from_date)
        employee_response['paid_to_date'] = '{:%Y-%m-%d}'.format(paid_to_date)
    else:
        employee_response['paid_from_date'] = paid_from_date.as_string()
        employee_response['paid_to_date'] = paid_to_date.as_string()
    employee_response['disable_input'] = False
    return employee_response


# Create your views here.
def payroll_entry(request):
    ko_data = {}
    ko_data['deduction_data'] = {}
    ko_data['incentive_data'] = {}
    ko_data['allowance_data'] = {}
    ko_data['calender'] = CALENDAR

    for name, id in get_deduction_names():
        ko_data['deduction_data']['deduction_%d' % (id)] = ''

    for name, id in get_incentive_names():
        ko_data['incentive_data']['incentive_%d' % (id)] = ''

    for name, id in get_allowance_names():
        ko_data['allowance_data']['allowance_%d' % (id)] = ''

    main_form = GroupPayrollForm(initial={'payroll_type': 'GROUP'})
    row_form = PaymentRowFormSet()[0]
    deduction_form = DeductionFormSet()[0]
    incentive_form = IncentiveFormSet()[0]
    allowance_form = AllowanceFormSet()[0]
    # underscore_row_form = get_underscore_formset(str(row_form))
    return render(
        request,
        'payroll_entry.html',
        {
          'r_form': row_form,
          'm_form': main_form,
          'deduction_form': deduction_form,
          'allowance_form': allowance_form,
          'incentive_form': incentive_form,
          'ko_data': ko_data
        })


def get_employee_account(request):
    response = {}
    error = {}
    if request.POST:
        employee_id = request.POST.get('paid_employee', None)
        if employee_id:
            employee = Employee.objects.get(id=int(employee_id))
        else:
            error['employee'] = 'No such employee'

        dates = verify_request_date(request)

        if isinstance(dates, tuple):
            paid_from_date, paid_to_date = dates
        else:
            error.update(dates)

        if error:
            response['errors'] = error
            return JsonResponse(response)

        # Now calculate all the values and give a good meaningful response
        # total_work_day = paid_to_date - paid_from_date
        response['data'] = get_employee_salary_detail(
            employee,
            paid_from_date,
            paid_to_date
        )

        # response.update(resp)
        return JsonResponse(response)
    else:
        return HttpResponse('Damn no request.POST')


def get_employees_account(request):
    error = {}
    response = {}
    data_list = []
    if request.POST:
        dates = verify_request_date(request)
        if isinstance(dates, tuple):
            paid_from_date, paid_to_date = dates
        else:
            error.update(dates)

        if error:
            response['errors'] = error
            return JsonResponse(response)

        branch = request.POST.get('branch', None)
        if branch:
            if branch == 'ALL':
                employees = Employee.objects.all()
            else:
                employees = Employee.objects.filter(
                    working_branch__id=int(branch)
                )

            for employee in employees:
                # data_dict = {'employee_id': employee.id}
                employee_salary_detail = get_employee_salary_detail(
                    employee,
                    paid_from_date,
                    paid_to_date
                )

                # data_dict.update(employee_salary_detail)
                data_list.append(employee_salary_detail)

            response['data'] = data_list
            return JsonResponse(response)


def test(request):
    emp = Employee.objects.get(id=1)
    x = BSDate(2072, 3, 1)
    y = BSDate(2072, 4, 32)

    salary = emp.current_salary_by_day(x, y)
    salary1 = emp.current_salary_by_month(x, y)
    pdb.set_trace()

    return HttpResponse(salary)


def save_payroll_entry(request):
    if request.POST:
        save_response = {}
        # pdb.set_trace()
        # pass
        row_count = request.POST('row_count', None)
        payment_records = []
        if row_count:
            for i in range(0, int(row_count)):

                # Similar if we need all details of incentive and allowence
                deductions = []
                for ded in Deduction.objects.all():
                    amount = request.POST.get('form-%d-deduction_%d' % (i, ded.id), None)
                    if amount:
                        deductions.append(DeductionDetail.objects.create(deduction_id=ded.id, amount=amount).id)
                allowances = []
                for allowance_name in AllowanceName.objects.all():
                    amount = request.POST.get('form-%d-allowance_%d' % (i, allowance_name.id), None)
                    if amount:
                        allowances.append(AllowanceDetail.objects.create(allowance_id=allowance_name.id, amount=amount).id)

                incentives = []
                for incentive_name in IncentiveName.objects.all():
                    amount = request.POST.get('form-%d-incentive_%d' % (i, incentive_name.id), None)
                    if amount:
                        incentives.append(IncentiveDetail.objects.create(incentive_id=incentive_name.id, amount=amount).id)

                p_r = PaymentRecord()
                p_r.paid_employee_id = int(request.POST.get('form-%d-paid_employee' % (i), None))

                # Save according to calender settin`g
                from_date = request.POST.get('form-%d-paid_from_date' % (i), None)
                to_date = request.POST.get('form-%d-paid_to_date' % (i), None)

                if(CALENDAR == 'AD'):
                    p_r.paid_from_date = datetime.strptime(from_date, '%Y-%m-%d')
                    p_r.paid_to_date = datetime.strptime(from_date, '%Y-%m-%d')
                else:
                    p_r.paid_from_date = from_date
                    p_r.paid_to_date = to_date

                p_r.absent_days = 0
                p_r.allowance = int(request.POST.get('form-%d-allowance' % (i), None))
                p_r.incentive = int(request.POST.get('form-%d-incentive' % (i), None))
                p_r.deduction_detail = deductions
                p_r.incentive_detail = incentives
                p_r.allowance_detail = allowances
                p_r.income_tax = int(request.POST.get('form-%d-income_tax' % (i), None))
                p_r.pro_tempore_amount = int(request.POST.get('form-%d-pro_tempore_amount' % (i), None))
                p_r.salary = int(request.POST.get('form-%d-salary' % (i), None))
                p_r.paid_amount = int(request.POST.get('form-%d-paid_amount' % (i), None))
                p_r.save()
                payment_records.append(p_r.id)
            PayrollEntry.objects.create(
                entry_row=payment_records,
            )
            save_response['entry_saved'] = True
            save_response['entry_approved'] = False
            save_response['entry_transacted'] = False
            return JsonResponse(save_response)


def get_employee_options(request):
    if request.POST:
        # pdb.set_trace()
        branch = request.POST.get('branch', None)
        if branch:
            if branch == 'ALL':
                employees = Employee.objects.all()
            else:
                employees = Employee.objects.filter(
                    working_branch__id=int(branch)
                )
            opt_list = [{'name': e.employee.full_name, 'id': e.id} for e in employees]
            return JsonResponse({'opt_data': opt_list})
        else:
            return HttpResponse('No branch')
    else:
        pdb.set_trace()
        return HttpResponse('No POST')