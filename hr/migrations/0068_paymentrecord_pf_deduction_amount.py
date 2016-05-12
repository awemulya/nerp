# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0067_auto_20160512_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='pf_deduction_amount',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
