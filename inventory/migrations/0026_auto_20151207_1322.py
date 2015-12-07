# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_auto_20151207_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instancehistory',
            name='from_location',
            field=models.ForeignKey(related_name='from_history', default=None, verbose_name='From Location', to='inventory.ItemLocation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instancehistory',
            name='to_location',
            field=models.ForeignKey(related_name='to_history', verbose_name='To Location', to='inventory.ItemLocation', null=True),
        ),
    ]
