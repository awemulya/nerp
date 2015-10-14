# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_release_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryaccount',
            name='opening_rate',
            field=models.FloatField(default=0),
        ),
    ]
