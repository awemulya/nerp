# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0028_auto_20160410_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeaccount',
            name='account_type',
            field=models.ForeignKey(default=1, to='hr.AccountType'),
        ),
    ]
