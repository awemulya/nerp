# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0068_paymentrecord_pf_deduction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='pf_monthly_deduction_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
