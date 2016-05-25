from django.db import models
from solo.models import SingletonModel


class KeySetting(SingletonModel):
    key = models.CharField(default='TRIAL', max_length=100)


# key_setting = KeySetting.get_solo()
