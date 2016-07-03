# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20160703_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aid',
            name='imprest_ledger',
            field=models.OneToOneField(related_name='imprest_for', to='account.Account'),
        ),
    ]
