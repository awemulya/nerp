# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151007_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='location',
            field=models.ForeignKey(default=1, to='inventory.ItemLocation'),
            preserve_default=False,
        ),
    ]
