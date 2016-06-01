# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20160526_1544'),
        ('hr', '0096_allowance_account_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allowance',
            name='account_category',
        ),
        migrations.AddField(
            model_name='allowancename',
            name='account_category',
            field=models.ForeignKey(blank=True, to='account.Category', null=True),
        ),
    ]
