from dbsettings.models import Setting
from django.shortcuts import redirect
from core.models import app_setting
from .coder import Coder

app_header_for_forms = app_setting.header_for_forms

DEFAULT_VALUE = 'NERP'
APP_NAME = 'NERP'
ATTR_NAME = 'header_for_forms'


def validate_key(key, user, app_name):
    from datetime import date

    parts = key.split('-')
    if len(parts) != 3:
        return False
    if not str(Coder.checksum(user)) == parts[0]:
        return False
    if not Coder.rot13(app_name) == parts[1]:
        return False
    try:
        if date.today() > Coder.decode_date(parts[2]):
            return False
    except ValueError:
        return False
    return True


class KeyMiddleware(object):
    def process_request(self, request):
        setting = Setting.objects.get(attribute_name=ATTR_NAME)
        if not setting.value == DEFAULT_VALUE and not request.path.replace('/', '')[0:5] == 'admin':
            valid = False
            try:
                key = Setting.objects.get(attribute_name='key')
                valid = validate_key(key.value, setting.value, APP_NAME)
            except Setting.DoesNotExist:
                pass
            if not valid:
                return redirect('/')
        pass
