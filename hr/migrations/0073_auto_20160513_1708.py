# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0072_auto_20160513_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='in_acc_type',
            field=models.ForeignKey(related_name='in_account_type', blank=True, to='hr.AccountType', null=True),
        ),
    ]
