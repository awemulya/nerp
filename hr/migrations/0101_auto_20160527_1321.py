# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0100_remove_employee_incentives'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='incentives',
            field=models.ManyToManyField(to='hr.IncentiveName', through='hr.Incentive', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='incentive',
            unique_together=set([('name', 'employee')]),
        ),
    ]
