# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20160510_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
