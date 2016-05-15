# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 07:57
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.deletion
import inventory.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0030_auto_20160224_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.PositiveIntegerField(verbose_name='Voucher No.')),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
            ],
        ),
        migrations.CreateModel(
            name='StockEntryRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit', models.CharField(default='pieces', max_length=50)),
                ('account_no', models.PositiveIntegerField()),
                ('opening_balance', models.FloatField(default=0)),
                ('opening_rate', models.FloatField(default=0)),
                ('opening_rate_vattable', models.BooleanField(default=True)),
                ('stock_entry', inventory.models.UnsavedForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='inventory.StockEntry')),
            ],
        ),
    ]