# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0062_auto_20160508_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='in_acc_type',
            field=models.ForeignKey(related_name='in_account_type', to='hr.AccountType'),
        ),
        migrations.AlterField(
            model_name='employeeaccount',
            name='account_type',
            field=models.ForeignKey(related_name='employee_account_type', to='hr.AccountType'),
        ),
    ]
