# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0048_auto_20151006_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationcomparison',
            name='report_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
