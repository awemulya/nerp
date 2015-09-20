# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_auto_20150920_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryreportrow',
            name='item',
            field=models.ForeignKey(default='', to='inventory.Item'),
            preserve_default=False,
        ),
    ]
