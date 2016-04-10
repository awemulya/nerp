# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0026_auto_20160409_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='accounts',
            field=models.ManyToManyField(to='hr.Account', through='hr.EmployeeAccount'),
        ),
        migrations.AlterField(
            model_name='employeeaccount',
            name='account',
            field=models.ForeignKey(to='hr.Account', unique=True),
        ),
    ]
