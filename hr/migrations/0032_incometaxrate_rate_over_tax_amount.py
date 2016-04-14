# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0031_paymentrecord_income_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='incometaxrate',
            name='rate_over_tax_amount',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
