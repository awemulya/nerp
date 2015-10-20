# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20151020_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('type', models.CharField(max_length=20, choices=[(b'Waive', 'Waive'), (b'Handover', 'Handover'), (b'Auction', 'Auction')])),
                ('rate', models.PositiveIntegerField(null=True, blank=True)),
                ('instance', models.ForeignKey(to='inventory.ItemInstance')),
            ],
        ),
    ]
