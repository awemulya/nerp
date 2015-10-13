# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def fiscal_years(apps, schema_editor):
    from core.models import FiscalYear
    # FiscalYear = apps.get_model('core', 'FiscalYear')
    FiscalYear.objects.create(year=2069)
    FiscalYear.objects.create(year=2070)
    FiscalYear.objects.create(year=2071)
    FiscalYear.objects.create(year=2072)
    FiscalYear.objects.create(year=2073)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fiscal_years),
    ]
