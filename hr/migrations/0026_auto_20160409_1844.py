# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0025_auto_20160409_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeaccount',
            name='account',
            field=models.ForeignKey(to='hr.Account'),
        ),
    ]
