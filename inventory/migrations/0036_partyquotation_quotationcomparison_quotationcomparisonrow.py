# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('inventory', '0035_auto_20150721_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyQuotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('per_unit_price', models.FloatField()),
                ('party', models.ForeignKey(related_name='party_quote', to='core.Party')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationComparison',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationComparisonRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=250)),
                ('quantity', models.FloatField()),
                ('estimated_cost', models.FloatField()),
                ('item', models.ForeignKey(related_name='item_quotation', to='inventory.Item')),
                ('party', models.ForeignKey(related_name='bidder_quote', to='inventory.PartyQuotation')),
                ('quotation', models.ForeignKey(related_name='rows', to='inventory.QuotationComparison')),
            ],
        ),
    ]
