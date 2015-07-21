# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0031_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('demand_row', models.ForeignKey(to='inventory.DemandRow')),
                ('item_instance', models.ForeignKey(to='inventory.ItemInstance')),
                ('location', models.ForeignKey(to='inventory.ItemLocation')),
            ],
        ),
    ]
