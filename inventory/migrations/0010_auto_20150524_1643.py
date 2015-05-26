# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_yearlyreport_yearlyreportrow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderrow',
            name='purchase_order',
            field=inventory.models.UnsavedForeignKey(related_name='rows', to='inventory.PurchaseOrder'),
        ),
    ]
