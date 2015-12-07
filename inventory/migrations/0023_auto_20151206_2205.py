# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_remove_yearlyreport_report_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yearlyreport',
            name='fiscal_year',
            field=models.ForeignKey(to='core.FiscalYear', unique=True),
        ),
    ]
