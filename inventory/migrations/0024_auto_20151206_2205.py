# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_auto_20151206_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yearlyreport',
            name='fiscal_year',
            field=models.OneToOneField(to='core.FiscalYear'),
        ),
    ]
