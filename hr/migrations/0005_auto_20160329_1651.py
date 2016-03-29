# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_auto_20160329_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_type',
        ),
        migrations.AddField(
            model_name='deduction',
            name='in_acc_type',
            field=models.OneToOneField(null=True, to='hr.AccountType'),
        ),
    ]
