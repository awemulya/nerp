# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackitem',
            name='item_rate',
            field=models.FloatField(null=True),
        ),
    ]
