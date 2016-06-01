# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import hr.models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0103_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeaccount',
            name='account',
            field=models.OneToOneField(related_name='employee_account', on_delete=django.db.models.deletion.PROTECT, validators=[hr.models.employee_account_validator], to='account.Account'),
        ),
        migrations.AlterField(
            model_name='employeeaccount',
            name='employee',
            field=models.ForeignKey(to='hr.Employee', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
