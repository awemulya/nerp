# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0030_auto_20160410_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='income_tax',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
