# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20160328_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='payed_amout',
            new_name='paid_amount',
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='payed_employee',
            new_name='paid_employee',
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='payed_from_date',
            new_name='paid_from_date',
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='payed_to_date',
            new_name='paid_to_date',
        ),
    ]
