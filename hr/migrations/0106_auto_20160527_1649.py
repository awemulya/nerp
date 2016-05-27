# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0105_auto_20160527_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyaccount',
            name='account',
        ),
        migrations.RemoveField(
            model_name='salaryaccount',
            name='account',
        ),
        migrations.DeleteModel(
            name='CompanyAccount',
        ),
        migrations.DeleteModel(
            name='SalaryAccount',
        ),
    ]
