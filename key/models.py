import dbsettings


class KeySettings(dbsettings.Group):
    key = dbsettings.TextValue(default='TRIAL')


key_setting = KeySettings()
