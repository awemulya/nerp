# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160516_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsetting',
            name='fiscal_year',
            field=models.PositiveIntegerField(default=2072, choices=[(2069, b'2069/70'), (2070, b'2070/71'), (2071, b'2071/72'), (2072, b'2072/73')]),
        ),
    ]
