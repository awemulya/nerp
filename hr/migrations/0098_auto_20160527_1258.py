# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20160526_1544'),
        ('hr', '0097_auto_20160527_1236'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AccountType',
        ),
        migrations.RemoveField(
            model_name='allowanceaccount',
            name='account',
        ),
        migrations.RemoveField(
            model_name='deductionaccount',
            name='account',
        ),
        migrations.RemoveField(
            model_name='incentiveaccount',
            name='account',
        ),
        migrations.AddField(
            model_name='incentivename',
            name='account_category',
            field=models.ForeignKey(blank=True, to='account.Category', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='incentive',
            unique_together=set([('name',)]),
        ),
        migrations.DeleteModel(
            name='AllowanceAccount',
        ),
        migrations.DeleteModel(
            name='DeductionAccount',
        ),
        migrations.RemoveField(
            model_name='incentive',
            name='account',
        ),
        migrations.RemoveField(
            model_name='incentive',
            name='employee_grade',
        ),
        migrations.DeleteModel(
            name='IncentiveAccount',
        ),
    ]
