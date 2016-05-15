# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0073_auto_20160513_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='pf_monthly_deduction_amount',
            field=models.FloatField(default=0),
        ),
    ]
