# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_auto_20151126_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depreciation',
            name='time',
            field=models.FloatField(default=0),
        ),
    ]
