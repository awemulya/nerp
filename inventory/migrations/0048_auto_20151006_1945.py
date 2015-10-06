# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0047_auto_20151006_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depreciation',
            name='time_type',
            field=models.CharField(default=b'years', max_length=8, choices=[(b'days', 'Day(s)'), (b'months', 'Month(s)'), (b'years', 'Year(s)')]),
        ),
    ]
