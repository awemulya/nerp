from dbsettings.models import Setting

# from django.http import HttpResponse
# from django.shortcuts import redirect
# from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

from .coder import Coder

from .config import *


def validate_key(key, user, app_name):
    from datetime import date

    parts = key.split('-')
    if len(parts) != 3:
        return {'error': 'Invalid key!'}
    if not str(Coder.checksum(user)) == parts[0]:
        return {'error': 'Key not valid for current user!'}
    if not Coder.rot13(app_name) == parts[1]:
        return {'error': 'Key not valid for current app!'}
    try:
        if date.today() > Coder.decode_date(parts[2]):
            return {'error': 'Key expired!'}
    except ValueError:
        return {'error': 'Invalid expiration date in key!'}
    return {'success': True}


class KeyMiddleware(object):
    def process_request(self, request):
        try:
            setting = Setting.objects.get(attribute_name=ATTR_NAME)
            if not setting.value in DEFAULT_VALUES and not request.path.replace('/', '')[
                                                           0:5] == 'admin' and not request.path.replace(
                    '/', '')[0:3] == 'key':
                validity = {'error': 'No Activation Key!'}
                try:
                    key = Setting.objects.get(attribute_name='key')
                    validity = validate_key(key.value, setting.value, APP_NAME)
                except Setting.DoesNotExist:
                    pass
                if 'error' in validity:
                    # return HttpResponse('<h2 style="text-align: center; margin-top: 20%">' + validity['error'] + '</h2>')
                    # return redirect(reverse_lazy('invalid_key'))
                    return render(request, 'key/invalid.html', validity)
        except Setting.DoesNotExist:
            pass
