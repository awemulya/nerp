# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0065_auto_20160509_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='pf_deduction_amount',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
