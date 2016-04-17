# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0034_protempore_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='pro_tempore_amount',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
