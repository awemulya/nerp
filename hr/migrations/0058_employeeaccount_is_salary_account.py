# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0057_auto_20160507_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeaccount',
            name='is_salary_account',
            field=models.BooleanField(default=False),
        ),
    ]
