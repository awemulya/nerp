import pdb

def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs


def empty_to_none(o):
    if o == '':
        return None
    return o


def all_empty(row, required_fields):
    empty = True
    for attr in required_fields:
        # if one of the required attributes isn received or is not an empty string
        if attr in row and row.get(attr) != "":
            empty = False
    return empty


def save_model(model, values):
    for key, value in values.iteritems():
        setattr(model, key, value)
    model.save()
    return model


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


def add(*args):
    total = 0
    for arg in args:
        if arg == '':
            arg = 0
        total += float(arg)
    return total


def title_case(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])
