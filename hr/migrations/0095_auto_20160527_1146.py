# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0094_auto_20160526_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allowance',
            name='account',
        ),
        migrations.AlterField(
            model_name='employee',
            name='optional_deduction',
            field=models.ManyToManyField(to='hr.Deduction', blank=True),
        ),
    ]
