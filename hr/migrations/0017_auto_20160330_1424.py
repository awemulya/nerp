# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0016_auto_20160330_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='explicit_acc',
            field=models.ForeignKey(blank=True, to='hr.Account', null=True),
        ),
        migrations.AlterField(
            model_name='deduction',
            name='in_acc_type',
            field=models.ForeignKey(to='hr.AccountType'),
        ),
    ]
