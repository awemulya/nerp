# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_account_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ('order',)},
        ),
    ]
