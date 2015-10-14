# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_entryreportrow_vattable'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryaccount',
            name='opening_rate_vattable',
            field=models.BooleanField(default=True),
        ),
    ]
