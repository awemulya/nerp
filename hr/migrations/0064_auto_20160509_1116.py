# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0063_auto_20160508_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeaccount',
            name='account_type',
        ),
        migrations.AddField(
            model_name='employeeaccount',
            name='account_meta_type',
            field=models.CharField(default='OTHER_ACCOUNT', max_length=100, choices=[(b'BANK_ACCOUNT', 'Employee Bank Account'), (b'OTHER_ACCOUNT', 'Other Employee Account')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeeaccount',
            name='other_account_type',
            field=models.ForeignKey(related_name='employee_account_type', blank=True, to='hr.AccountType', null=True),
        ),
    ]
