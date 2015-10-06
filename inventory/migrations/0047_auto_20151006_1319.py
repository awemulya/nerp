# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0046_auto_20151006_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminstance',
            name='location',
            field=models.ForeignKey(to='inventory.ItemLocation'),
        ),
    ]
