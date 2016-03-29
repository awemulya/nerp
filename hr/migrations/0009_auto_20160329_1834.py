# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_auto_20160329_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowence',
            name='incentive_cycle',
            field=models.CharField(max_length=50, null=True, choices=[(b'M', 'Monthly'), (b'Y', 'Yearly'), (b'D', 'Daily'), (b'H', 'Hourly')]),
        ),
        migrations.AddField(
            model_name='incentive',
            name='incentive_cycle',
            field=models.CharField(max_length=50, null=True, choices=[(b'M', 'Monthly'), (b'Y', 'Yearly'), (b'D', 'Daily'), (b'H', 'Hourly')]),
        ),
    ]
