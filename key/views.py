import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import requests

from django.http import JsonResponse
# from dbsettings.models import Setting
from key.models import KeySetting

from .config import *


def send_key_request(request):
    # setting = Setting.objects.get(attribute_name=ATTR_NAME)
    setting = getattr(KeySetting.get_solo(), ATTR_NAME)
    res = requests.post(REQUEST_URL, data={'app': APP_NAME, 'user': setting})
    return JsonResponse(json.loads(res.content))


def invalid_key(request):
    return render(request, 'key/invalid.html')


@csrf_exempt
def activation(request):
    if request.POST.get('key'):
        # try:
            # key = Setting.objects.get(attribute_name='key')
        key_setting = KeySetting.get_solo()
        # key = getattr(key_setting, 'key')
        # except Setting.DoesNotExist:
            # key = Setting.objects.create(attribute_name='key', module_name='key.models')

        setattr(key_setting, 'key', request.POST.get('key'))
        key_setting.save()
        if request.META.get('HTTP_REFERER'):
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('/')
