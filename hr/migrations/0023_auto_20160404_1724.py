# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0022_auto_20160404_1655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='sanchai_account',
            new_name='sanchayakosh_account',
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(unique=True, max_length=150, choices=[(b'BANK ACCOUNT', 'Bank Account'), (b'INSURANCE ACCOUNT', 'InsuranceAccount'), (b'NALAKOSH ACCOUNT', 'Nagarik Lagani Kosh Account'), (b'SANCHAYAKOSH ACCOUNT', 'Sanchaya Kosh')]),
        ),
    ]
