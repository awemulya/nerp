# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0069_auto_20160512_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incometaxrate',
            name='rate_over_tax_amount',
        ),
    ]
