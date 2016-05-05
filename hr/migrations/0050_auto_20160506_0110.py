# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0049_auto_20160506_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='allowances',
            field=models.ManyToManyField(to='hr.AllowanceName', blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='incentives',
            field=models.ManyToManyField(to='hr.IncentiveName', blank=True),
        ),
    ]
