# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0081_auto_20160517_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maritalstatus',
            name='marital_status',
            field=models.CharField(default=b'U', unique=True, max_length=1, choices=[(b'M', 'Married'), (b'U', 'Unmarried')]),
        ),
    ]
