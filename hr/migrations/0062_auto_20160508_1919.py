# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0061_auto_20160508_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='account',
            field=models.OneToOneField(related_name='allowance_account', null=True, blank=True, to='hr.AllowanceAccount'),
        ),
        migrations.AlterField(
            model_name='deduction',
            name='account',
            field=models.OneToOneField(related_name='deduction_account', null=True, blank=True, to='hr.DeductionAccount'),
        ),
        migrations.AlterField(
            model_name='incentive',
            name='account',
            field=models.OneToOneField(related_name='incentive_account', null=True, blank=True, to='hr.IncentiveAccount'),
        ),
    ]
