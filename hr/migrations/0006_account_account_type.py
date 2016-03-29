# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_auto_20160329_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(to='hr.AccountType', null=True),
        ),
    ]
