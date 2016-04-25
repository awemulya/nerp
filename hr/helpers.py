from datetime import date
from bsdate import BSDate


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
