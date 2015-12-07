# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_auto_20151206_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instancehistory',
            name='from_location',
            field=models.ForeignKey(related_name='from_history', verbose_name='From Location', to='inventory.ItemLocation', null=True),
        ),
    ]
