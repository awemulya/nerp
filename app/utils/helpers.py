from django.db import connection
import socket
import urllib
import json
from datetime import date


def fetch_npr_conversion(from_date, to_date=None, currency=None):
    if from_date > date.today():
        raise ValueError("We can't forecast, nor travel to future.")
    url = 'http://nrb.org.np/exportForexJSON.php?YY=' + str(from_date.year) + '&MM=' + str(from_date.month).zfill(
        2) + '&DD=' + str(from_date.day).zfill(2)
    if to_date:
        url += '&YY1=' + str(to_date.year) + '&MM1=' + str(to_date.month).zfill(2) + '&DD1=' + str(to_date.day).zfill(2)
    response = urllib.urlopen(url)
    data = json.loads(response.read()).get('Conversion').get('Currency')
    if currency and not to_date:
        return next(obj for obj in data if obj.get('BaseCurrency') == currency)
    return data


def truncate_model(model):
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE " + model._meta.db_table + " CASCADE;")


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex.message
        return False


def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "" or row.get(attr) is None:
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
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model


def zero_for_none(obj):
    if obj is None or obj is '':
        return 0
    else:
        return obj


def float_zero_for_none(obj):
    if obj is None or obj is '':
        return 0
    else:
        return float(obj)


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


def model_exists_in_db(model):
    return model._meta.db_table in connection.introspection.table_names()


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
