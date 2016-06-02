# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0110_remove_paymentrecord_pf_deduction_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incentive',
            name='amount_editable',
        ),
        migrations.AddField(
            model_name='incentivename',
            name='amount_editable',
            field=models.BooleanField(default=False),
        ),
    ]
