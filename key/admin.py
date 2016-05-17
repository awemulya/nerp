from django.contrib import admin
from solo.admin import SingletonModelAdmin
from key.models import KeySetting


class MSingletonAdmin(SingletonModelAdmin):
    change_form_template = 'key/change_form.html'

admin.site.register(KeySetting, MSingletonAdmin)
