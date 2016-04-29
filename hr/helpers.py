from datetime import date
from bsdate import BSDate
from njango.nepdate import bs
from calendar import monthrange as mr


def get_y_m_tuple_list(from_date, to_date):
    return_list = []
    while from_date <= to_date:
        return_list.append((from_date.year, from_date.month))
        if from_date.month < 12:
            if type(from_date) == date:
                from_date = date(
                    from_date.year,
                    from_date.month + 1,
                    from_date.day
                )
            else:
                from_date = BSDate(
                    from_date.year,
                    from_date.month + 1,
                    from_date.day
                )
        else:
            if type(from_date) == date:
                from_date = date(
                    from_date.year + 1,
                    1,
                    from_date.day
                )
            else:
                from_date = BSDate(
                    from_date.year + 1,
                    1,
                    from_date.day
                )
    return return_list


def are_side_months(from_date, to_date):
    if from_date.year == to_date.year and to_date.month - from_date.month == 1:
        return True
    elif to_date.year - from_date.year == 1 and from_date.month - to_date.month == 11:
        return True
    else:
        return False


def bs_str2tuple(date_string):
    as_list = date_string.split('-')
    date_tuple = (
        int(as_list[0]),
        int(as_list[1]),
        int(as_list[2])
    )
    # If possible varify this
    return date_tuple


def get_account_id(employee_object, account_type):
    from hr.models import EmployeeAccount
    return EmployeeAccount.objects.get(
        employee=employee_object,
        account_type__name=account_type
    ).account.id


def delta_month_date(p_from, p_to):
    y_m_tuple = get_y_m_tuple_list(p_from, p_to)
    total_month = len(y_m_tuple)
    total_work_day = 0
    if isinstance(p_from, date):
        if type(p_from) == type(p_to):
            for mon in y_m_tuple:
                total_work_day += mr(*mon)[1]
    else:
        if type(p_from) == type(p_to):
            for mon in y_m_tuple:
                total_work_day += bs[mon[0]][mon[1] - 1]
                # total_work_day += mr(*mon)[1]
    return (total_month, total_work_day)


def delta_month_date_impure(p_from, p_to):
    if type(p_from) == type(p_to):
        if p_from.year == p_to.year and p_from.month == p_to.month:
            total_days = (p_to - p_from).days + 1
            if isinstance(p_from, date):
                pure_month_days = mr(p_from.year, p_from.month)[1]
            else:
                pure_month_days = bs[p_from.year][p_from.month - 1]
            total_month = total_days / pure_month_days

        elif are_side_months(p_from, p_to):
            pure_month_days = 0

            if isinstance(p_from, date):
                lhs_month = date(p_from.year, p_from.month, 1)
                rhs_month = date(p_to.year, p_to.month, 1)
                lhs_month_work_days = (rhs_month - p_from).days
                rhs_month_work_days = (p_to - rhs_month).days + 1

                lhs_month_days = mr(lhs_month.year, lhs_month.month)[1]
                rhs_month_days = mr(rhs_month.year, rhs_month.month)[1]

            else:
                lhs_month = BSDate(p_from.year, p_from.month, 1)
                rhs_month = BSDate(p_to.year, p_to.month, 1)
                lhs_month_work_days = (rhs_month - p_from).days
                rhs_month_work_days = (p_to - rhs_month).days + 1

                lhs_month_days = bs[lhs_month.year][lhs_month.month - 1]
                rhs_month_days = bs[rhs_month.year][rhs_month.month - 1]
            total_month = (lhs_month_work_days / lhs_month_days) + (rhs_month_work_days / rhs_month_days)
            total_days = lhs_month_work_days + rhs_month_work_days
        else:
            if isinstance(p_from, date):
                if p_from.month == 12:
                    p_from_m = date(p_from.year + 1, 1, 1)
                else:
                    p_from_m = date(p_from.year, p_from.month + 1, 1)
                if p_to.month == 1:
                    p_to_m = date(p_to.year - 1, 12, 1)
                else:
                    p_to_m = date(p_to.year, p_to.month - 1, 1)
                lhs_month = date(p_from.year, p_from.month, 1)
                rhs_month = date(p_to.year, p_to.month, 1)
                lhs_month_work_days = (p_from_m - p_from).days
                rhs_month_work_days = (p_to - p_to_m).days + 1

                lhs_month_days = mr(lhs_month.year, lhs_month.month)[1]
                rhs_month_days = mr(rhs_month.year, rhs_month.month)[1]

            else:
                if p_from.month == 12:
                    p_from_m = BSDate(p_from.year + 1, 1, 1)
                else:
                    p_from_m = BSDate(p_from.year, p_from.month + 1, 1)
                if p_to.month == 1:
                    p_to_m = BSDate(p_to.year - 1, 12, 1)
                else:
                    p_to_m = BSDate(p_to.year, p_to.month - 1, 1)
                lhs_month = BSDate(p_from.year, p_from.month, 1)
                rhs_month = BSDate(p_to.year, p_to.month, 1)
                lhs_month_work_days = (p_from_m - p_from).days
                rhs_month_work_days = (p_to - p_to_m).days + 1

                lhs_month_days = bs[lhs_month.year][lhs_month.month - 1]
                rhs_month_days = bs[rhs_month.year][rhs_month.month - 1]

            y_m_tuple = get_y_m_tuple_list(p_from_m, p_to_m)
            total_month = len(y_m_tuple) + (lhs_month_work_days / lhs_month_days) + (rhs_month_work_days / rhs_month_days)
            total_days = (p_to - p_from).days + 1
    return (total_month, total_days)


def empty_to_none(o):
    if o == '':
        return None
    return o


def empty_to_zero(o):
    if o == '' or o == None:
        return 0
    return o


def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj
