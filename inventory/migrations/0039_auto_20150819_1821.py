# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0038_auto_20150819_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationcomparisonrow',
            name='specification',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
