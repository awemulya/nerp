# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0109_auto_20160602_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrecord',
            name='pf_deduction_amount',
        ),
    ]
