# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151007_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiscalyear',
            name='year',
            field=models.IntegerField(unique=True, choices=[(2069, b'2069/70'), (2070, b'2070/71'), (2071, b'2071/72'), (2072, b'2072/73')]),
        ),
    ]
