import dbsettings

class AppSetting(dbsettings.Group):
    site_name = dbsettings.StringValue(default='NERP')
    fiscal_year = dbsettings.ForeignKeyValue(app='core', model='FiscalYear')
    header_for_forms = dbsettings.TextValue()


app_setting = AppSetting()