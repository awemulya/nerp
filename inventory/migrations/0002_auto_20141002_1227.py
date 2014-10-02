# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='account',
            field=models.OneToOneField(related_name=b'item', null=True, to='inventory.InventoryAccount'),
        ),
    ]
