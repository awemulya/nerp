# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0019_auto_20160404_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='priority',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
