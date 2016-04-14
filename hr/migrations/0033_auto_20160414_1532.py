# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0032_incometaxrate_rate_over_tax_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='incometaxrate',
            name='is_last',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='incometaxrate',
            name='end_to',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
