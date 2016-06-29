# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_data_fy'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgethead',
            name='recurrent',
            field=models.BooleanField(default=True),
        ),
    ]
