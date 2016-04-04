# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0020_deduction_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='priority',
            field=models.IntegerField(unique=True),
        ),
    ]
