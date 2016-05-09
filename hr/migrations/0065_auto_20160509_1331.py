# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0064_auto_20160509_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(unique=True, max_length=150, choices=[(b'insurance_account', 'Insurance Account'), (b'nalakosh_account', 'Nagarik Lagani Kosh Account'), (b'sanchayakosh_account', 'Sanchayakosh Account')]),
        ),
    ]
