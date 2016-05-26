# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0085_auto_20160525_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeaccount',
            name='account_meta_type',
        ),
        migrations.RemoveField(
            model_name='employeeaccount',
            name='is_salary_account',
        ),
        migrations.RemoveField(
            model_name='employeeaccount',
            name='other_account_type',
        ),
    ]
