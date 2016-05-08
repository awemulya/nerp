# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0060_auto_20160508_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowance',
            name='account',
            field=models.OneToOneField(null=True, blank=True, to='hr.AllowanceAccount'),
        ),
        migrations.AddField(
            model_name='deduction',
            name='account',
            field=models.OneToOneField(null=True, blank=True, to='hr.DeductionAccount'),
        ),
        migrations.AddField(
            model_name='incentive',
            name='account',
            field=models.OneToOneField(null=True, blank=True, to='hr.IncentiveAccount'),
        ),
    ]
