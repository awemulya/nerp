# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20160526_1544'),
        ('hr', '0088_auto_20160526_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='deduct_in_category',
            field=models.ForeignKey(blank=True, to='account.Category', null=True),
        ),
    ]
