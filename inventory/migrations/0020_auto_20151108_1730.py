# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20151104_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='fiscal_year',
        ),
        migrations.RemoveField(
            model_name='entryreport',
            name='fiscal_year',
        ),
        migrations.RemoveField(
            model_name='handover',
            name='fiscal_year',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='fiscal_year',
        ),
        migrations.RemoveField(
            model_name='quotationcomparison',
            name='fiscal_year',
        ),
    ]
