import dbsettings
from django.db import models
from solo.models import SingletonModel


class KeySettingsDb(dbsettings.Group):
    key = dbsettings.TextValue(default='TRIAL')


key_setting = KeySettingsDb()


class KeySetting(SingletonModel):
    key = models.CharField(default='TRIAL', max_length=100)
