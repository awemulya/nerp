from __future__ import division

import json

from django.db import transaction

from app import settings
from core.models import FiscalYear
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType

from hr.serializers import PayrollEntrySerializer
from .forms import GroupPayrollForm, EmployeeIncentiveFormSet, EmployeeForm, \
    IncentiveNameForm, IncentiveNameFormSet, AllowanceNameForm, AllowanceNameFormSet, \
    TaxSchemeForm, TaxCalcSchemeFormSet, TaxSchemeFormSet, MaritalStatusForm, IncentiveNameDetailFormSet, GetReportForm, \
    EmployeeGradeFormSet, EmployeeGradeGroupFormSet, DesignationFormSet, ReportHrForm, ReportHrTableFormSet, \
    DeductionNameFormSet, GradeScaleValidityForm, AllowanceValidityForm, DeductionValidityForm
from .models import Employee, Deduction, EmployeeAccount, TaxScheme, ProTempore, IncentiveName, AllowanceName, \
    DeductionDetail, AllowanceDetail, IncentiveDetail, PaymentRecord, PayrollEntry, Account, Incentive, Allowance, \
    MaritalStatus, ReportHR, BranchOffice, EmployeeGrade, EmployeeGradeGroup, Designation, DeductionName, \
    AllowanceValidity, DeductionValidity, GradeScaleValidity
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from calendar import monthrange as mr
from njango.nepdate import bs
from .models import get_y_m_tuple_list
from .bsdate import BSDate
from .helpers import are_side_months, bs_str2tuple, get_account_id, delta_month_date, delta_month_date_impure, \
    emp_salary_eligibility, month_cnt_inrange, fiscal_year_data, employee_last_payment_record, \
    emp_salary_eligibility_on_edit, get_validity_slots, get_validity_id
from account.models import set_transactions
from hr.filters import EmployeeFilter
from django.core import serializers

from hr.models import ACC_CAT_BASIC_SALARY_ID, \
    ACC_CAT_SALARY_GIVING_ID, \
    ACC_CAT_PRO_TEMPORE_ID, \
    ACC_CAT_TAX_ID

CALENDAR = settings.HR_CALENDAR

# Taxation singleton setting dbsettings
F_TAX_DISCOUNT_LIMIT = 300000
M_TAX_DISCOUNT_LIMIT = 200000
SOCIAL_SECURITY_TAX_RATE = 1


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



        if paid_from_date:
            error['global_errors'] = []
            try:
                get_validity_id(GradeScaleValidity, paid_from_date)
            except IOError:
                error['global_errors'].append(
                    _('Given from date is to early for given Grade Scale Validities')
                )

            try:
                get_validity_id(AllowanceValidity, paid_from_date)
            except IOError:
                error['global_errors'].append(
                    _('Given from date is to early for given Allowance Validities')
                )

            try:
                get_validity_id(DeductionValidity, paid_from_date)
            except IOError:
                error['global_errors'].append(
                    _('Given from date is to early for given Deduction Validities')
                )

            if paid_to_date:
                if paid_to_date < paid_from_date:
                    error['global_errors'].append(
                        _('Date: paid to must be greater than paid from')
                    )
            if not error['global_errors']:
                del error['global_errors']


        if error:
            return error
        else:
            monthly_payroll = request.POST.get(
                'is_monthly_payroll',
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


def salary_taxation_unit(employee, f_y_item):
    # if CALENDAR == 'BS':
    #     CURRENT_FISCAL_YEAR = (
    #         BSDate(*FiscalYear.start()),
    #         BSDate(*FiscalYear.end())
    #     )


    # First calculate all the uncome of employee
    total_month, total_work_day = delta_month_date_impure(
        *f_y_item['f_y']
    )
    salary = employee.get_date_range_salary(
        *f_y_item['f_y'],
        apply_grade_rate=True
    )
    scale_salary = employee.get_date_range_salary(
        *f_y_item['f_y']
    )

    deductions = DeductionName.objects.all()

    allowance = 0
    allowance_validity_slots = get_validity_slots(AllowanceValidity, f_y_item['f_y'][0], f_y_item['f_y'][1])
    for ob in employee.allowances.all():

        for slot in allowance_validity_slots:
            total_month, total_work_day = delta_month_date_impure(
                slot.from_date,
                slot.to_date
            )

            try:
                obj = ob.allowances.all().filter(
                    employee_grade=employee.designation.grade,
                    validity_id=slot.validity_id
                )[0]
            except IndexError:
                raise IndexError('%s not defined for grade %s' % (ob.name, employee.designation.grade.grade_name))
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                cnt = month_cnt_inrange(
                    obj.year_payment_cycle_month,
                    slot.from_date,
                    slot.to_date
                )
                if cnt:
                    if obj.sum_type == 'AMOUNT':
                        allowance += obj.value * cnt
                    else:
                        allowance += obj.value / 100.0 * scale_salary

            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    allowance += obj.value * total_month
                else:
                    allowance += obj.value / 100.0 * scale_salary
            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    allowance += obj.value * total_work_day
                else:
                    # Does this mean percentage in daily wages
                    allowance += obj.value / 100.0 * scale_salary

    # now calculate incentive if it has but not to add to salary just to
    # transact seperately
    incentive = 0
    for ob in employee.incentives.all():
        try:
            obj = ob.incentives.filter(
                employee=employee
            )[0]
        except IndexError:
            raise IndexError('%s not defined for grade %s' % (ob.name, employee.designation.grade.grade_name))
        if obj.payment_cycle == 'Y':
            # check obj.year_payment_cycle_month to add to salary
            cnt = month_cnt_inrange(
                obj.year_payment_cycle_month,
                **f_y_item['f_y']
            )
            if cnt:
                if obj.sum_type == 'AMOUNT':
                    incentive += obj.value * cnt
                else:
                    incentive += obj.value / 100.0 * scale_salary

        elif obj.payment_cycle == 'M':
            if obj.sum_type == 'AMOUNT':
                incentive += obj.value * total_month
            else:
                incentive += obj.value / 100.0 * scale_salary
        elif obj.payment_cycle == 'D':
            if obj.sum_type == 'AMOUNT':
                incentive += obj.value * total_work_day
            else:
                # Does this mean percentage in daily wages
                incentive += obj.value / 100.0 * scale_salary

    total_deduction = 0
    deduction = 0
    for obj in deductions.filter(is_tax_free=True):
        if obj in deductions.filter(is_optional=False) or obj in employee.optional_deductions.all():
            for slot in get_validity_slots(DeductionValidity, f_y_item['f_y'][0], *f_y_item['f_y'][1]):
                deduct_obj = Deduction.objects.filter(validity_id=slot.validity_id, name=obj)[0]
                if deduct_obj.deduct_type == 'AMOUNT':
                    deduction = obj.value * total_month
                    total_deduction += deduction
                else:
                    deduction = obj.value / 100.0 * salary
                    total_deduction += deduction

                if employee.is_permanent and obj.is_refundable_deduction:
                    # This is for addition of refundable deduction
                    total_deduction += deduction

    taxable_amount = (salary + allowance + incentive - total_deduction)

    if employee.sex == 'F':
        taxable_amount -= F_TAX_DISCOUNT_LIMIT
    else:
        taxable_amount -= M_TAX_DISCOUNT_LIMIT

    if taxable_amount < 0:
        taxable_amount = 0

    social_security_tax = SOCIAL_SECURITY_TAX_RATE / 100 * taxable_amount

    taxable_amount -= social_security_tax
    tax_amount = 0
    tax_schemes = sorted(
        TaxScheme.objects.filter(
            marital_status__marital_status=employee.marital_status
        ), key=lambda obj: obj.priority)
    main_loop_break_flag = False
    for obj in tax_schemes:
        # if obj.end_to:

        if (taxable_amount >= obj.start_from and
                    taxable_amount <= obj.end_to if obj.end_to else True):
            tax_calc_scheme = sorted(
                obj.tax_calc_scheme.all(),
                key=lambda x: x.priority
            )
            for obj2 in tax_calc_scheme:
                if obj.end_to != obj2.end_to:
                    tax_amount += obj2.end_to * obj2.tax_rate / 100
                    taxable_amount -= obj2.end_to
                else:
                    tax_amount += taxable_amount * obj2.tax_rate / 100
                    main_loop_break_flag = True
                    break
        if main_loop_break_flag:
            break
    total_tax = social_security_tax + tax_amount
    return total_tax * (f_y_item['worked_days'] / f_y_item['year_days'])


def get_employee_salary_detail(employee, paid_from_date, paid_to_date, eligibility_check_on_edit, edit_row):
    row_errors = []
    if not eligibility_check_on_edit:
        eligible, error = emp_salary_eligibility(
            employee,
            paid_from_date,
            paid_to_date,
        )

    else:
        eligible, error = emp_salary_eligibility_on_edit(
            paid_from_date,
            paid_to_date,
            employee,
            edit_row
        )
    if not eligible:
        row_errors.append(error)

    employee_response = {}
    employee_response['paid_employee'] = str(employee.id)
    employee_response['employee_grade'] = employee.designation.grade.grade_name
    employee_response['employee_designation'] = employee.designation.designation_name

    # This should be in if when we combine both monthly and daily payroll
    total_month, total_work_day = delta_month_date_impure(
        paid_from_date,
        paid_to_date
    )

    salary = employee.get_date_range_salary(
        paid_from_date,
        paid_to_date,
        apply_grade_rate=True
    )
    scale_salary = employee.get_date_range_salary(
        paid_from_date,
        paid_to_date
    )
    deductions = DeductionName.objects.all()

    # # Addition of PF and bima to salary if employee is permanent
    # addition_pf = 0
    # for item in deductions:
    #     if employee.is_permanent:
    #         if item.add2_init_salary:
    #             if item.deduct_type == 'AMOUNT':
    #                 addition_pf += item.value * total_month
    #             else:
    #                 # Rate
    #                 addition_pf += item.value / 100.0 * salary

    # Now add allowance to the salary(salary = salary + allowance)
    # Question here is do we need to deduct from incentove(I gues not)
    allowance_validity_slots = get_validity_slots(AllowanceValidity, paid_from_date, paid_to_date)
    allowance = 0
    # for obj in employee.allowances.all():
    employee_response['allowance_details'] = []
    allowance_details = employee_response['allowance_details']
    for _name in employee.allowances.all():

        allowance_details.append({
            'amount': 0
        })

        for slot in allowance_validity_slots:
            try:
                obj = _name.allowances.all().filter(
                    employee_grade=employee.designation.grade,
                    validity_id=slot.validity_id
                )[0]
            except IndexError:
                raise IndexError('%s not defined for grade %s' % (_name.name, employee.designation.grade.grade_name))
            # if obj:
            #     obj = obj[0]

            total_month, total_work_day = delta_month_date_impure(
                slot.from_date,
                slot.to_date
            )

            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary
                cnt = month_cnt_inrange(
                    obj.year_payment_cycle_month,
                    slot.from_date,
                    slot.to_date
                )
                if cnt:
                    if obj.sum_type == 'AMOUNT':
                        allowance_details[-1]['amount'] += obj.value * cnt
                    else:
                        allowance_details[-1]['amount'] += obj.value / 100.0 * scale_salary
                else:
                    allowance_details[-1]['amount'] += 0

            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    allowance_details[-1]['amount'] += obj.value * total_month
                else:
                    allowance_details[-1]['amount'] += obj.value / 100.0 * scale_salary


            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    allowance_details[-1]['amount'] += obj.value * total_work_day

                else:
                    allowance_details[-1]['amount'] += obj.value / 100.0 * scale_salary

                    # Does this mean percentage in daily wages
                    # else:
                    #     # This is hourly case(Dont think we have it)
                    #     pass
                    # else:
                    #     # Here also same as below
                    #     employee_response['allowance_%d' % (_name.id)] = 0
            allowance += allowance_details[-1]['amount']
        allowance_details[-1]['allowance'] = _name.id
        allowance_details[-1]['name'] = _name.name

    employee_response['allowance'] = allowance
    # salary += allowance

    # now calculate incentive if it has but not to add to salary just to
    # transact seperately
    incentive = 0
    # for obj in employee.incentives.all():

    employee_response['incentive_details'] = []
    incentive_details = employee_response['incentive_details']

    for _name in employee.incentives.all():
        try:
            obj = _name.incentives.all().filter(employee=employee)[0]
        except IndexError:
            raise IndexError('%s not defined for grade %s' % (_name.name, employee.full_name))
            # if obj:
            #     obj = obj[0]
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
                    incentive_details.append({
                        'amount': obj.value * cnt
                    })
                else:
                    incentive_details.append({
                        'amount': obj.value / 100.0 * scale_salary
                    })
            else:
                incentive_details.append({
                    'amount': 0
                })

        elif obj.payment_cycle == 'M':
            if obj.sum_type == 'AMOUNT':
                incentive_details.append({
                    'amount': obj.value * total_month
                })
            else:
                incentive_details.append({
                    'amount': obj.value / 100.0 * scale_salary
                })
        elif obj.payment_cycle == 'D':
            if obj.sum_type == 'AMOUNT':
                incentive_details.append({
                    'amount': obj.value * total_work_day
                })
            else:
                # Does this mean percentage in daily wages
                incentive_details.append({
                    'amount': obj.value / 100.0 * scale_salary
                })
        else:
            # This is hourly case(Dont think we have it)
            incentive_details.append({
                'amount': 0
            })
            # else:
            #     employee_response['incentive_%d' % (_name.id)] = 0
        # Here we should check for scale and calculate from scale
        if _name.with_scale:
            # Get scale here for this employee of this incentive and get value that is
            # scale = none
            # employee_response['incentive_%d' % (_name.id)] = scale / 100 * employee_response['incentive_%d' % (_name.id)]
            pass
        incentive_details[-1]['incentive'] = _name.id
        incentive_details[-1]['name'] = _name.name
        incentive_details[-1]['editable'] = True if _name.amount_editable else False
        incentive += incentive_details[-1]['amount']
    employee_response['incentive'] = incentive
    # salary += incentive

    # Now the deduction part from the salary
    deduction_validity_slots = get_validity_slots(DeductionValidity, paid_from_date, paid_to_date)
    deduction = 0
    employee_response['deduction_details'] = []
    deduction_details = employee_response['deduction_details']
    for obj in list(deductions.filter(is_optional=False)) + list(employee.optional_deductions.all()):
        deduction_details.append({
            'amount': 0
        })
        for slot in deduction_validity_slots:
            deduct_obj = Deduction.objects.filter(validity_id=slot.validity_id, name=obj)[0]
            total_month, total_work_day = delta_month_date_impure(
                slot.from_date,
                slot.to_date
            )
            if deduct_obj.deduct_type == 'AMOUNT':
                deduction_details[-1]['amount'] += obj.value * total_month
            else:
                deduction_details[-1]['amount'] += obj.value / 100.0 * salary

            if employee.is_permanent and obj.is_refundable_deduction:
                salary += deduction_details[-1]['amount']
                deduction_details[-1]['amount'] += deduction_details[-1]['amount'] * 2

            deduction += deduction_details[-1]['amount']
        deduction_details[-1]['deduction'] = obj.id
        deduction_details[-1]['name'] = obj.name
        deduction_details[-1]['editable'] = True if obj.amount_editable else False

    employee_response['deduced_amount'] = deduction

    # PF deduction amount in case of loan from PF

    # Income tax logic
    f_y_data = fiscal_year_data(paid_from_date, paid_to_date)
    income_tax = 0
    for item in f_y_data:
        income_tax += salary_taxation_unit(
            employee,
            item
        )

    employee_response['income_tax'] = income_tax
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
    employee_response['salary'] = salary
    # employee_response['employee_bank_account_id'] = get_account_id(
    #     employee, 'bank_account')

    # employee_response['paid_amount'] = salary - deduction - income_tax + \
    #                                    p_t_amount + incentive + allowance

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
    employee_response['disable_input'] = True
    # employee_response['emp_options'] = []
    employee_response['emp_options'] = [{
        'id': employee.id,
        'name': employee.employee.full_name,
    }]
    return employee_response


# Create your views here.
def payroll_entry(request, pk=None):
    if pk:
        entry = PayrollEntry.objects.get(pk=pk)
        serializer = PayrollEntrySerializer(entry)
        ctx_data = dict(serializer.data)
    else:
        ctx_data = {'edit': False,}
    main_form = GroupPayrollForm(initial={'payroll_type': 'GROUP'})

    # Inititial employee options
    employees = Employee.objects.all()
    emp_opt_list = [{'name': e.name, 'id': str(e.id)} for e in employees]

    ko_data = {
        'ctx_data': ctx_data,
        'emp_options': emp_opt_list
    }

    return render(
        request,
        'payroll_entry.html',
        {
            'm_form': main_form,
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

        edit = request.POST.get('edit')
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

        # Check for eligibility check
        eligibility_check_on_edit = False
        edit_row = None
        if edit:
            p_e = PayrollEntry.objects.get(id=edit)
            emp_entry_rows = p_e.entry_rows.all().filter(paid_employee=employee)
            if not emp_entry_rows:
                eligibility_check_on_edit = False
            else:
                eligibility_check_on_edit = True
                edit_row = emp_entry_rows[0]

        response['data'] = get_employee_salary_detail(
            employee,
            paid_from_date,
            paid_to_date,
            eligibility_check_on_edit,
            edit_row
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
        edit = request.POST.get('edit')
        if branch == 'ALL':
            employees = Employee.objects.all()
        else:
            employees = Employee.objects.filter(
                working_branch__id=int(branch)
            )

        for employee in employees:
            # data_dict = {'employee_id': employee.id}
            eligibility_check_on_edit = False
            edit_row = None
            if edit:
                p_e = PayrollEntry.objects.get(id=edit)
                emp_entry_rows = p_e.entry_rows.all().filter(paid_employee=employee)
                if not emp_entry_rows:
                    eligibility_check_on_edit = False
                else:
                    eligibility_check_on_edit = True
                    edit_row = emp_entry_rows[0]
            employee_salary_detail = get_employee_salary_detail(
                employee,
                paid_from_date,
                paid_to_date,
                eligibility_check_on_edit,
                edit_row
            )

            # data_dict.update(employee_salary_detail)
            data_list.append(employee_salary_detail)

        response['data'] = data_list
        return JsonResponse(response)


def save_payroll_entry(request, pk=None):
    if pk:
        p_e = PayrollEntry.objects.get(id=pk)
    else:
        p_e = PayrollEntry()
    if request.POST:
        params = json.loads(request.body)
        save_response = {}

        is_monthly_payroll = True if params.get('is_monthly_payroll', None) else False
        # if branch is ALL then save it as None
        request_branch = params.get('branch', None)
        branch = None if request_branch == 'ALL' else int(request_branch)

        payment_records = []

        with transaction.atomic():

            for row in params.get('entry_rows'):

                if row.get('id'):
                    p_r = PaymentRecord.objects.get(id=row.get('id'))
                    p_r.deduction_details.all().delete()
                    p_r.incentive_details.all().delete()
                    p_r.allowance_details.all().delete()
                else:
                    p_r = PaymentRecord

                # Similar if we need all details of incentive and allowence
                deductions = []
                for ded in row.get('deduction_details', []):
                    amount = float(ded['amount'])
                    if amount:
                        deductions.append(DeductionDetail.objects.create(deduction_id=ded['deduction'], amount=amount))
                allowances = []
                for allowance_name in row.get('allowance_details', []):
                    amount = float(allowance_name['amount'])
                    if amount:
                        allowances.append(
                            AllowanceDetail.objects.create(allowance_id=allowance_name['allowance'], amount=amount))

                incentives = []
                for incentive_name in row.get('incentive_details', []):
                    amount = float(incentive_name['amount'])
                    if amount:
                        incentives.append(
                            IncentiveDetail.objects.create(incentive_id=incentive_name['incentive'], amount=amount))

                # p_r = PaymentRecord()
                p_r.paid_employee_id = int(row.get('paid_employee', None))

                # Save according to calender settin`g
                # from_date = request.POST.get('form-%d-paid_from_date' % (i), None)
                # to_date = request.POST.get('form-%d-paid_to_date' % (i), None)

                if (CALENDAR == 'AD'):
                    p_r.paid_from_date = datetime.strptime(row.get('paid_from_date'), '%Y-%m-%d')
                    p_r.paid_to_date = datetime.strptime(row.get('paid_from_date'), '%Y-%m-%d')
                else:
                    p_r.paid_from_date = row.get('paid_from_date')
                    p_r.paid_to_date = row.get('paid_to_date')

                p_r.absent_days = row.get('absent_days', 0)
                p_r.deduced_amount = float(row.get('deduced_amount', None))

                p_r.allowance = float(row.get('allowance', None))
                p_r.incentive = float(row.get('incentive', None))
                p_r.income_tax = float(row.get('income_tax', None))
                p_r.pro_tempore_amount = float(row.get('pro_tempore_amount', None))
                p_r.salary = float(row.get('salary', None))
                p_r.paid_amount = float(row.get('paid_amount', None))
                p_r.save()
                p_r.deduction_details.add(*deductions)
                p_r.incentive_details.add(*incentives)
                p_r.allowance_details.add(*allowances)

                payment_records.append(p_r.id)
            # p_e = PayrollEntry()
            p_e.branch_id = branch
            p_e.is_monthly_payroll = is_monthly_payroll
            p_e.save()
            p_e.entry_rows.add(*payment_records)
            # PayrollEntry.objects.create(
            #     entry_row=payment_records,
            # )
            save_response['entry_id'] = p_e.id
            save_response['entry_saved'] = True
            save_response['entry_approved'] = False
            save_response['entry_transacted'] = False
            return JsonResponse(save_response)  # Should have permissions


def approve_entry(request, pk=None):
    payroll_entry = PayrollEntry.objects.get(pk=pk)
    payroll_entry.approved = True
    payroll_entry.save()
    if request.is_ajax():
        return JsonResponse({'entry_approved': True})
    else:
        return redirect(reverse('entry_list'))


# Should have permissions
def delete_entry(request, pk=None):
    payroll_entry = PayrollEntry.objects.get(pk=pk)
    payment_records_rows = payroll_entry.entry_rows.all()
    payment_recordid_set = [p.id for p in payment_records_rows]
    # pdb.set_trace()
    # payroll_entry.entry_row_set.clear()

    # Delete Transaction Here
    # delete_rows(
    #     payment_records_rows,
    #     PaymentRecord
    # )

    payroll_entry.delete()

    for pr_id in payment_recordid_set:
        p_r = PaymentRecord.objects.get(id=pr_id)
        record_deduction_details = [rdd.id for rdd in p_r.deduction_details.all()]
        record_allowance_details = [rad.id for rad in p_r.allowance_details.all()]
        record_incentive_details = [rid.id for rid in p_r.incentive_details.all()]

        try:
            JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(PaymentRecord),
                                     object_id=p_r.id).delete()
        except:
            pass

        p_r.delete()

        for rdd_id in record_deduction_details:
            DeductionDetail.objects.get(id=rdd_id).delete()
        for rad_id in record_allowance_details:
            AllowanceDetail.objects.get(id=rad_id).delete()
        for rid_id in record_incentive_details:
            IncentiveDetail.objects.get(id=rid_id).delete()
    return redirect(reverse('entry_list'))


def entry_detail(request, pk=None):
    # ko_data contains entry main properties
    ko_data = {}

    rows = []

    all_allowances = AllowanceName.objects.all()
    all_incentives = IncentiveName.objects.all()
    all_deductions = Deduction.objects.all()

    allowance_titles = []
    incentive_titles = []
    deduction_titles = []

    for ob in all_allowances:
        a_title = _(ob.name.title())
        allowance_titles.append(a_title)
    for ob in all_incentives:
        i_title = _(ob.name.title())
        incentive_titles.append(i_title)
    for ob in all_deductions:
        # if ob.deduction_for == 'EMPLOYEE ACC':
        #     d_name = '_'.join(ob.in_acc_type.name.split(' ')).lower()
        # else:
        d_name = '_'.join(ob.name.split(' ')).lower()
        d_title = ' '.join(d_name.split('_')).title()
        deduction_titles.append(d_title)

    if pk:
        p_e = PayrollEntry.objects.get(id=pk)
        ko_data['entry_id'] = p_e.id
        ko_data['entry_approved'] = p_e.approved
        ko_data['entry_transacted'] = p_e.transacted

        entry_rows = p_e.entry_rows.all()

        paid_from_date = entry_rows[0].paid_from_date
        paid_to_date = entry_rows[0].paid_to_date
        branch = p_e.branch.name if p_e.branch else "From All Branch"

        if isinstance(paid_from_date, date):
            paid_from_date = '{:%Y/%m/%d}'.format(entry_rows[0].paid_from_date)
            paid_to_date = '{:%Y/%m/%d}'.format(entry_rows[0].paid_from_date)

        for row in entry_rows:
            entry_row_data = {}
            emp = row.paid_employee
            entry_row_data['employee'] = (emp)
            entry_row_data['employee_designation'] = (row.paid_employee.designation)
            entry_row_data['employee_grade'] = (row.paid_employee.designation.grade)

            allowance_amounts = []
            for obj in all_allowances:
                a_amount = 0
                for allowance_n, amount in [(a.allowance, a.amount) for a in row.allowance_details.all()]:
                    if obj == allowance_n:
                        a_amount = amount
                        break
                allowance_amounts.append(a_amount)
            entry_row_data['allowance_data'] = allowance_amounts
            entry_row_data['total_allowance'] = (row.allowance)

            incentive_amounts = []
            for obj in all_incentives:
                i_amount = 0
                for incentive_n, amount in [(a.incentive, a.amount) for a in row.incentive_details.all()]:
                    if obj == incentive_n:
                        i_amount = amount
                        break
                incentive_amounts.append(i_amount)
            entry_row_data['incentive_data'] = incentive_amounts
            entry_row_data['total_incentive'] = (row.incentive)

            deduction_amounts = []
            for obj in all_deductions:
                d_amount = 0
                for deduction, amount in [(a.deduction, a.amount) for a in row.deduction_details.all()]:
                    if obj == deduction:
                        d_amount = amount
                        break
                deduction_amounts.append(d_amount)
            entry_row_data['deduction_data'] = deduction_amounts
            entry_row_data['deduced_amount'] = row.deduced_amount

            entry_row_data['income_tax'] = (row.income_tax)
            entry_row_data['pro_tempore_amount'] = (row.pro_tempore_amount)
            entry_row_data['salary'] = (row.salary)
            entry_row_data['paid_amount'] = (row.paid_amount)
            rows.append(entry_row_data)

        return render(
            request,
            'entry_detail.html',
            {
                'paid_from_date': paid_from_date,
                'paid_to_date': paid_to_date,
                'branch': branch,
                'rows': rows,
                'allowance_titles': allowance_titles,
                'incentive_titles': incentive_titles,
                'deduction_titles': deduction_titles,
                'ko_data': ko_data
            }
        )


def entry_list(request):
    entries = PayrollEntry.objects.all()
    return render(
        request,
        'entry_list.html',
        {
            'objects': entries,
        }
    )
    pass


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
            opt_list = [{'name': e.name, 'id': str(e.id)} for e in employees]
            return JsonResponse({'opt_data': opt_list})
        else:
            return HttpResponse('No branch')
    else:
        return HttpResponse('No POST')


def transact_entry(request, pk=None):
    p_e = PayrollEntry.objects.get(id=pk)

    for entry in p_e.entry_rows.all():
        employee = entry.paid_employee
        salary = entry.salary

        salary_giving_account = Account.objects.get(
            category_id=ACC_CAT_SALARY_GIVING_ID,
            name='SalaryGivingAccount'
        )

        # NeedUpdate
        # Later This will be one by its fiscal year
        emp_basic_salary_account = Account.objects.get(
            category_id=ACC_CAT_BASIC_SALARY_ID,
            employee_account__employee=employee
        )
        # First ma slary and allowance transact grade_name
        # SET TRANSACTION HERE FOR SALARY: DR IN EMP ACC
        set_transactions(
            entry,
            p_e.entry_datetime,
            *[
                ('cr', salary_giving_account, salary),
                ('dr', emp_basic_salary_account, salary),
            ]
        )

        # Transact Pro Tempore
        protempore_account = Account.objects.get(
            category_id=ACC_CAT_PRO_TEMPORE_ID,
            employee_account__employee=employee
        )
        pro_tempore_amount = entry.pro_tempore_amount

        set_transactions(
            entry,
            p_e.entry_datetime,
            *[
                ('cr', salary_giving_account, pro_tempore_amount),
                ('dr', protempore_account, pro_tempore_amount),
            ]
        )

        set_transactions(
            entry,
            p_e.entry_datetime,
            *[
                ('cr', protempore_account, pro_tempore_amount),
                ('dr', emp_basic_salary_account, pro_tempore_amount),
            ]
        )

        for allowance_details_item in entry.allowance_details.all():
            a_account = Account.objects.get(
                category=allowance_details_item.allowance.account_category,
                employee_account__employee=employee
            )
            a_amount = allowance_details_item.amount

            # Should be changed
            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    ('cr', salary_giving_account, a_amount),
                    ('dr', a_account, a_amount),
                ]
            )
            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    # ('dr', employee_salary_account, a_amount),
                    ('cr', a_account, a_amount),
                    ('dr', emp_basic_salary_account, a_amount),
                ]
            )

        for incentive_details_item in entry.incentive_details.all():
            i_account = Account.objects.get(
                category=incentive_details_item.incentive.account_category,
                employee_account__employee=employee
            )
            i_amount = incentive_details_item.amount

            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    ('cr', salary_giving_account, i_amount),
                    ('dr', i_account, i_amount),
                ]
            )
            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    ('cr', i_account, i_amount),
                    ('dr', emp_basic_salary_account, i_amount),
                ]
            )

        for deduction_details_item in entry.deduction_details.all():
            deduction_obj = deduction_details_item.deduction
            d_account = a_account = Account.objects.get(
                category=deduction_obj.deduct_in_category,
                employee_account__employee=employee
            )
            d_amount = deduction_details_item.amount

            set_transactions(
                entry,
                p_e.entry_datetime,
                *[
                    ('cr', emp_basic_salary_account, d_amount),
                    ('dr', d_account, d_amount),
                ]
            )

        # Transact Tax
        emp_tax_account = Account.objects.get(
            category_id=ACC_CAT_TAX_ID,
            employee_account__employee=employee
        )
        tax_amount = entry.income_tax

        set_transactions(
            entry,
            p_e.entry_datetime,
            *[
                ('cr', emp_basic_salary_account, tax_amount),
                ('dr', emp_tax_account, tax_amount),
            ]
        )

        set_transactions(
            entry,
            p_e.entry_datetime,
            *[
                ('cr', emp_tax_account, tax_amount),
                ('dr', salary_giving_account, tax_amount),
            ]
        )

    p_e.transacted = True
    p_e.save()
    if request.is_ajax():
        return JsonResponse({'entry_transacted': True})
    else:
        return redirect(reverse('entry_list'))


def employee(request, pk=None):
    ko_data = {}

    if pk:
        obj_id = pk
        employee = Employee.objects.get(id=pk)
    else:
        obj_id = None
        employee = Employee()

    if request.method == "POST":
        employee_form = EmployeeForm(request.POST, instance=employee)
        employee_incentive_formset = EmployeeIncentiveFormSet(request.POST, instance=employee)
        if employee_form.is_valid() and employee_incentive_formset.is_valid():
            employee_form.save()
            employee_incentive_formset.save()
            return redirect(reverse('list_employee'))
    else:
        employee_form = EmployeeForm(instance=employee)
        employee_incentive_formset = EmployeeIncentiveFormSet(instance=employee)

    return render(
        request,
        'employee_cu.html',
        {
            'employee_form': employee_form,
            'employee_incentive_formset': employee_incentive_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


def list_employee(request):
    objects = EmployeeFilter(request.GET, queryset=Employee.objects.all())
    return render(
        request,
        'employee_list.html',
        {
            'objects': objects,
        }
    )


def toggle_employee_activeness(request, pk=None):
    obj = Employee.objects.get(id=pk)
    # employee_accounts = EmployeeAccount.objects.filter(employee=obj)
    if obj.is_active:
        obj.is_active = False
    else:
        obj.is_active = True
    obj.save()
    # for emp_acc in employee_accounts:
    #     emp_acc.delete()
    return redirect(reverse('list_employee'))


# def incentive(request, pk=None):
#     ko_data = {}

#     if pk:
#         obj_id = pk
#         incentive_name = IncentiveName.objects.get(id=pk)
#     else:
#         obj_id = None
#         incentive_name = IncentiveName()

#     if request.method == "POST":
#         incentive_name_form = IncentiveNameForm(request.POST, instance=incentive_name)
#         incentive_formset = IncentiveNameFormSet(request.POST, instance=incentive_name)
#         if incentive_name_form.is_valid() and incentive_formset.is_valid():
#             incentive_name_form.save()
#             incentive_formset.save()
#             return redirect(reverse('list_incentive'))
#     else:
#         incentive_name_form = IncentiveNameForm(instance=incentive_name)
#         incentive_formset = IncentiveNameFormSet(instance=incentive_name)

#     return render(
#         request,
#         'incentive_cu.html',
#         {
#             'incentive_name_form': incentive_name_form,
#             'incentive_formset': incentive_formset,
#             'ko_data': ko_data,
#             'obj_id': obj_id,
#         })


# def list_incentive(request):
#     objects = IncentiveName.objects.all()
#     return render(
#         request,
#         'incentive_list.html',
#         {
#             'objects': objects,
#         }
#     )


# def delete_incentive(request, pk=None):
#     obj = IncentiveName.objects.get(id=pk)
#     # inc_details = Incentive.objects.filter(name=obj)
#     obj.delete()
#     # for inc in inc_details():
#     #     inc.delete()
#     return redirect(reverse('list_incentive'))


def allowance(request, pk=None):
    allowance_validity_form = AllowanceValidityForm()
    return render(
        request,
        'allowance.html',
        {
            'calendar': CALENDAR,
            'av_form': allowance_validity_form
        }
    )


def deduction_name(request):
    if request.method == "POST":

        deduction_formset = DeductionNameFormSet(
            request.POST,
            queryset=DeductionName.objects.all(),
        )
        if deduction_formset.is_valid():
            deduction_formset.save()
            return redirect(reverse('deduction_name'))
    else:
        deduction_formset = DeductionNameFormSet(
            queryset=DeductionName.objects.all(),
        )
    return render(
        request,
        'deduction_cu.html',
        {
            'deduction_formset': deduction_formset,
        })


def deduction(request):
    deduction_validity_form = DeductionValidityForm()
    return render(
        request,
        'deduction.html',
        {
            'dv_form': deduction_validity_form
        }
    )


def employee_grade(request):
    if request.method == "POST":

        employee_grade_formset = EmployeeGradeFormSet(
            request.POST,
            queryset=EmployeeGrade.objects.all(),
        )
        if employee_grade_formset.is_valid():
            employee_grade_formset.save()
            return redirect(reverse('employee_grade'))
    else:
        employee_grade_formset = EmployeeGradeFormSet(
            queryset=EmployeeGrade.objects.all(),
        )

    return render(
        request,
        'employee_grade_cu.html',
        {
            'employee_grade_formset': employee_grade_formset,
        })


def employee_grade_group(request):
    if request.method == "POST":

        employee_grade_group_formset = EmployeeGradeGroupFormSet(
            request.POST,
            queryset=EmployeeGradeGroup.objects.all(),
        )
        if employee_grade_group_formset.is_valid():
            employee_grade_group_formset.save()
            return redirect(reverse('employee_grade_group'))
    else:
        employee_grade_group_formset = EmployeeGradeGroupFormSet(
            queryset=EmployeeGradeGroup.objects.all(),
        )

    return render(
        request,
        'employee_grade_group_cu.html',
        {
            'employee_grade_group_formset': employee_grade_group_formset,
        })


def employee_designation(request):
    if request.method == "POST":

        designation_formset = DesignationFormSet(
            request.POST,
            queryset=Designation.objects.all(),
        )
        if designation_formset.is_valid():
            designation_formset.save()
            return redirect(reverse('employee_designation'))
    else:
        designation_formset = DesignationFormSet(
            queryset=Designation.objects.all(),
        )

    return render(
        request,
        'employee_designation_cu.html',
        {
            'designation_formset': designation_formset,
        })


def tax_scheme_detail(request, pk=None):
    ko_data = {}

    if pk:
        obj_id = pk
        tax_scheme = TaxScheme.objects.get(id=pk)
    else:
        obj_id = None
        tax_scheme = TaxScheme()

    if request.method == "POST":
        tax_scheme_form = TaxSchemeForm(request.POST, instance=tax_scheme)
        tax_calc_scheme_formset = TaxCalcSchemeFormSet(request.POST, instance=tax_scheme)
        if tax_scheme_form.is_valid() and tax_calc_scheme_formset.is_valid():
            tax_scheme_form.save()
            tax_calc_scheme_formset.save()
            return redirect(reverse('list_tax_scheme'))
    else:
        tax_scheme_form = TaxSchemeForm(instance=tax_scheme)
        tax_calc_scheme_formset = TaxCalcSchemeFormSet(instance=tax_scheme)

    return render(
        request,
        'tax_detail_scheme_cu.html',
        {
            'tax_scheme_form': tax_scheme_form,
            'tax_calc_scheme_formset': tax_calc_scheme_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


def list_tax_scheme(request):
    m_objects = sorted(
        TaxScheme.objects.filter(marital_status__marital_status='M'),
        key=lambda x: x.priority
    )
    u_objects = sorted(
        TaxScheme.objects.filter(marital_status__marital_status='U'),
        key=lambda x: x.priority
    )
    return render(
        request,
        'tax_scheme_list.html',
        {
            'm_objects': m_objects,
            'u_objects': u_objects,
        }
    )


# def delete_tax_scheme(request, pk=None):
#     obj = TaxScheme.objects.get(id=pk)
#     # alw_details = Allowance.objects.filter(name=obj)
#     obj.delete()
#     # for alw in alw_details():
#     #     alw.delete()
#     return redirect(reverse('list_tax_scheme'))


def tax_scheme(request, pk=None):
    ko_data = {}

    if pk:
        obj_id = pk
        marital_status = MaritalStatus.objects.get(id=pk)
    else:
        obj_id = None
        marital_status = MaritalStatus()

    if request.method == "POST":
        marital_status_form = MaritalStatusForm(request.POST, instance=marital_status)
        tax_scheme_formset = TaxSchemeFormSet(request.POST, instance=marital_status)
        if marital_status_form.is_valid() and tax_scheme_formset.is_valid():
            marital_status_form.save()
            tax_scheme_formset.save()
            return redirect(reverse('list_tax_scheme'))
    else:
        marital_status_form = MaritalStatusForm(instance=marital_status)
        tax_scheme_formset = TaxSchemeFormSet(instance=marital_status)

    return render(
        request,
        'tax_scheme_cu.html',
        {
            'marital_status_form': marital_status_form,
            'tax_scheme_formset': tax_scheme_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


def delete_taxscheme(request, pk=None):
    obj = MaritalStatus.objects.get(id=pk)
    # alw_details = Allowance.objects.filter(name=obj)
    obj.delete()
    # for alw in alw_details():
    #     alw.delete()
    return redirect(reverse('list_tax_scheme'))


def incentivename_curd(request):
    if request.method == "POST":

        incentivename_formset = IncentiveNameDetailFormSet(
            request.POST,
            queryset=IncentiveName.objects.all(),
        )
        if incentivename_formset.is_valid():
            incentivename_formset.save()
            return redirect(reverse('incentivename_curd'))
    else:
        incentivename_formset = IncentiveNameDetailFormSet(
            queryset=IncentiveName.objects.all(),
        )

    return render(
        request,
        'incentivename_curd.html',
        {
            'incentivename_formset': incentivename_formset,
        })


def get_report(request):
    if request.method == "POST":
        report_request_query = GetReportForm(request.POST, calendar=CALENDAR)
        if report_request_query.is_valid():
            report = report_request_query.cleaned_data.get('report')
            branch = report_request_query.cleaned_data.get('branch')
            from_date = report_request_query.cleaned_data.get('from_date')
            to_date = report_request_query.cleaned_data.get('to_date')

            if branch:
                branch_qry = {'paid_employee__working_branch': branch}
            else:
                branch_qry = {}
            payment_records = PaymentRecord.objects.filter(
                paid_from_date__gte=from_date,
                paid_to_date__lte=to_date,
                **branch_qry)
            template_path = '/'.join(report.template.split('/')[-2:])

            # create table data here
            report_tables = report.report_tables.all()
            for table in report_tables:
                fields = table.table_fields
                import ipdb
                ipdb.set_trace()

            return render(request, template_path, {})

        else:
            return render(request, 'get_report.html', {'get_report_form': report_request_query})
    else:
        get_report_form = GetReportForm()
        return render(request, 'get_report.html', {'get_report_form': get_report_form})


def report_setting(request, pk=None):
    ko_data = {}

    if pk:
        obj_id = pk
        hr_report = ReportHR.objects.get(id=pk)
    else:
        obj_id = None
        hr_report = ReportHR()

    if request.method == "POST":
        hr_report_form = ReportHrForm(request.POST, instance=hr_report)
        hr_report_table_formset = ReportHrTableFormSet(request.POST, instance=hr_report)
        if hr_report_form.is_valid() and hr_report_table_formset.is_valid():
            hr_report_form.save()
            hr_report_table_formset.save()
            return redirect(reverse('list_report_setting'))
    else:
        hr_report_form = ReportHrForm(instance=hr_report)
        hr_report_table_formset = ReportHrTableFormSet(instance=hr_report)
    # import ipdb
    # ipdb.set_trace()

    return render(
        request,
        'hr_report_cu.html',
        {
            'hr_report_form': hr_report_form,
            'hr_report_table_formset': hr_report_table_formset,
            'ko_data': ko_data,
            'obj_id': obj_id,
        })


def list_report_setting(request):
    objects = ReportHR.objects.all()
    return render(
        request,
        'hr_report_list.html',
        {
            'objects': objects,
        }
    )


def delete_report_setting(request, pk=None):
    obj = ReportHR.objects.get(id=pk)
    # alw_details = Allowance.objects.filter(name=obj)
    obj.delete()
    # for alw in alw_details():
    #     alw.delete()
    return redirect(reverse('list_allowance'))


# GradeScale Validity Crud

# End GradeScale Validity Crud


def grades_scale(request):
    grade_scale_validity_form = GradeScaleValidityForm()
    return render(request, 'grades_scale.html', {
        'gsv_form': grade_scale_validity_form
    })


# def generate_report(request):
#     if request.method == "POST":
#         report_request_query = GetReportForm(request.POST, calendar=CALENDAR)
#         if report_request_query.is_valid():
#             report = report_request_query.cleaned_data.get('report')
#             branch = report_request_query.cleaned_data.get('branch')
#             from_date = report_request_query.cleaned_data.get('from_date')
#             to_date = report_request_query.cleaned_data.get('to_date')
#
#             if branch:
#                 branch_qry = {'paid_employee__working_branch': branch}
#             else:
#                 branch_qry = {}
#             payment_records = PaymentRecord.objects.filter(
#                 paid_from_date__gte=from_date,
#                 paid_to_date__lte=to_date,
#                 **branch_qry)
#             import ipdb
#             ipdb.set_trace()
#             template_path = '/'.join(report.template.split('/')[-2:])
#             return render(request, template_path, {})
#
#         else:
#             return render(request, 'get_report.html', {'get_report_form': report_request_query})

def payroll_index(request):
    return render(request, 'hr_index.html', {})
