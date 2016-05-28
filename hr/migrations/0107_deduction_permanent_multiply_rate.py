# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0106_auto_20160527_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='permanent_multiply_rate',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
