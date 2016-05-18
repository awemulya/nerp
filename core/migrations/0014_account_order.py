# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_account_fy'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
