# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0036_transaction_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='salary',
            field=models.FloatField(null=True, blank=True),
        ),
    ]