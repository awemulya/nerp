# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0006_account_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(to='hr.AccountType'),
        ),
        migrations.AlterField(
            model_name='deduction',
            name='in_acc_type',
            field=models.OneToOneField(to='hr.AccountType'),
        ),
    ]
