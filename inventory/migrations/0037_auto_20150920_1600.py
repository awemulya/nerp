# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0036_auto_20150920_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryreportrow',
            name='item',
            field=models.ForeignKey(blank=True, to='inventory.Item', null=True),
        ),
    ]
