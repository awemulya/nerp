# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0052_auto_20160506_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='payment_cycle',
            field=models.CharField(max_length=50, choices=[(b'M', 'Monthly'), (b'Y', 'Yearly'), (b'D', 'Daily')]),
        ),
        migrations.AlterField(
            model_name='allowancedetail',
            name='Incentive',
            field=models.ForeignKey(related_name='allowance_amount_detail', to='hr.AllowanceName'),
        ),
        migrations.AlterField(
            model_name='incentive',
            name='payment_cycle',
            field=models.CharField(max_length=50, choices=[(b'M', 'Monthly'), (b'Y', 'Yearly'), (b'D', 'Daily')]),
        ),
        migrations.AlterField(
            model_name='incentivedetail',
            name='Incentive',
            field=models.ForeignKey(related_name='incentive_amount_detail', to='hr.IncentiveName'),
        ),
    ]
