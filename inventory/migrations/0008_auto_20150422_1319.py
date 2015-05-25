# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20150422_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yearlyreport',
            name='fiscal_year',
        ),
        migrations.RemoveField(
            model_name='yearlyreportrow',
            name='yearly_report',
        ),
        migrations.DeleteModel(
            name='YearlyReport',
        ),
        migrations.DeleteModel(
            name='YearlyReportRow',
        ),
    ]
