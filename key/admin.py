from django.contrib import admin
from solo.admin import SingletonModelAdmin
from key.models import KeySetting

admin.site.register(KeySetting, SingletonModelAdmin)
