import json

import requests

from django.http import JsonResponse
from dbsettings.models import Setting

from .config import *


def send_key_request(request):
    setting = Setting.objects.get(attribute_name=ATTR_NAME)
    res = requests.post(REQUEST_URL, data={'app': APP_NAME, 'user': setting.value})
    return JsonResponse(json.loads(res.content))
