# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0018_auto_20160404_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allowence',
            old_name='incentive_cycle',
            new_name='payment_cycle',
        ),
        migrations.RenameField(
            model_name='allowence',
            old_name='year_allowence_cycle_month',
            new_name='year_payment_cycle_month',
        ),
        migrations.RenameField(
            model_name='incentive',
            old_name='incentive_cycle',
            new_name='payment_cycle',
        ),
        migrations.RenameField(
            model_name='incentive',
            old_name='year_incentive_cycle_month',
            new_name='year_payment_cycle_month',
        ),
    ]
