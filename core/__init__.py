import dbsettings
from .models import FiscalYear

class AppSetting(dbsettings.Group):
    site_name = dbsettings.StringValue(default='NERP')
    fiscal_year = dbsettings.ForeignKeyValue(model=FiscalYear)
    header_for_forms = dbsettings.TextValue()


app_setting = AppSetting()