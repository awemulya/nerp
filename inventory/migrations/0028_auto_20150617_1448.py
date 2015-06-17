# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_item_depreciation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depreciation',
            name='time_type',
            field=models.CharField(default=b'Year(s)', max_length=8, choices=[(b'Day(s)', 'Day(s)'), (b'Month(s)', 'Month(s)'), (b'Year(s)', 'Year(s)')]),
        ),
    ]
