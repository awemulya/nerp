# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_inventoryaccount_opening_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='entryreportrow',
            name='vattable',
            field=models.BooleanField(default=True),
        ),
    ]
