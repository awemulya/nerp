# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0111_auto_20160602_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incentive',
            name='sum_type',
            field=models.CharField(max_length=50),
        ),
    ]