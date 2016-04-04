# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0021_auto_20160404_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttype',
            name='permanent_multiply_rate',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(unique=True, max_length=150, choices=[(b'BANK ACC', 'Bank Account'), (b'INSURANCE ACC', 'InsuranceAccount'), (b'NALA ACC', 'Nagarik Lagani Kosh Account'), (b'SANCHAYA KOSH', 'Sanchaya Kosh')]),
        ),
    ]
