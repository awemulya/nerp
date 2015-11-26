# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_auto_20151207_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depreciation',
            name='depreciate_value',
            field=models.FloatField(default=0),
        ),
    ]
