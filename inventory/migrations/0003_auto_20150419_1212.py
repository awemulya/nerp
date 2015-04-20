# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_itemlocation_trackitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandrow',
            name='location',
            field=models.ForeignKey(blank=True, to='inventory.ItemLocation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='demandrow',
            name='purpose',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
