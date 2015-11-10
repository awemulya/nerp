# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20151108_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yearlyreport',
            name='report_no',
        ),
    ]
