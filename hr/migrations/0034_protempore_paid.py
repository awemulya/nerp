# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0033_auto_20160414_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='protempore',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
