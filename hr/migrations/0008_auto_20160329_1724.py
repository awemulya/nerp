# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_auto_20160329_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(unique=True, max_length=150, choices=[(b'BANK ACC', 'Bank Account'), (b'INSURANCE ACC', 'InsuranceAccount'), (b'NALA ACC', 'Nagarik Lagani Kosh Account'), (b'SANCHAI KOSH', 'Sanchai Kosh')]),
        ),
    ]
