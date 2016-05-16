# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImprestTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, choices=[(b'initial_deposit', b'Initial Deposit'), (b'gon_fund_transfer', b'GON Fund Transfer'), (b'replenishment_received', b'Replenishment Received'), (b'payment', b'Payment'), (b'liquidation', b'Liquidation')])),
                ('date', models.DateField(null=True, blank=True)),
                ('wa_no', models.CharField(max_length=10, null=True, verbose_name=b'Withdrawal Application No.', blank=True)),
                ('ref', models.CharField(max_length=10, null=True, verbose_name=b'Reference', blank=True)),
                ('amount', models.FloatField()),
                ('description', models.TextField(null=True, blank=True)),
                ('exchange_rate', models.FloatField(null=True, blank=True)),
                ('currency', models.ForeignKey(to='core.Currency')),
                ('fy', models.ForeignKey(to='core.FiscalYear')),
            ],
        ),
    ]
