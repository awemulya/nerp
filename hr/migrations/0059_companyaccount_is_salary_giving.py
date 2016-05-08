# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0058_employeeaccount_is_salary_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyaccount',
            name='is_salary_giving',
            field=models.BooleanField(default=False),
        ),
    ]
