# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0101_auto_20160527_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='incentivename',
            name='with_scale',
            field=models.BooleanField(default=False),
        ),
    ]
