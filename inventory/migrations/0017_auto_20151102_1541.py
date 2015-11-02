# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20151028_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='rate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(default=b'consumable', max_length=15, choices=[(b'consumable', 'Consumable'), (b'non-consumable', 'Non-consumable')]),
        ),
    ]
