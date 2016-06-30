# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20160630_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetallocationitem',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='budgetreleaseitem',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='disbursementdetail',
            name='disbursement_method',
            field=models.CharField(max_length=255, choices=[(b'direct_payment', b'Direct Payment'), (b'reimbursement', b'Reimbursement'), (b'replenishment', b'Replenishment'), (b'liquidation', b'Liquidation')]),
        ),
        migrations.AlterField(
            model_name='expenditure',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
