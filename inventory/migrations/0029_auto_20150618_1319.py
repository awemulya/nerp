# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_auto_20150617_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='depreciation',
            field=models.ForeignKey(related_name='depreciate_item', blank=True, to='inventory.Depreciation', null=True),
        ),
    ]
