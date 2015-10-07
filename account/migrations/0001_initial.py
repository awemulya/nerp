# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
            ],
        ),
        migrations.CreateModel(
            name='JournalVoucherRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.PositiveIntegerField(null=True, blank=True)),
                ('cr_amount', models.PositiveIntegerField(null=True, blank=True)),
                ('account', models.ForeignKey(to='core.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('no', models.PositiveIntegerField()),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('invoice_no', models.PositiveIntegerField(null=True, blank=True)),
                ('vattable', models.BooleanField(default=False)),
                ('nepal_government', models.FloatField(null=True, blank=True)),
                ('foreign_cash_grant', models.FloatField(null=True, blank=True)),
                ('foreign_compensating_grant', models.FloatField(null=True, blank=True)),
                ('foreign_cash_loan', models.FloatField(null=True, blank=True)),
                ('foreign_compensating_loan', models.FloatField(null=True, blank=True)),
                ('foreign_substantial_aid', models.FloatField(null=True, blank=True)),
                ('advanced', models.FloatField(null=True, blank=True)),
                ('advanced_settlement', models.FloatField(null=True, blank=True)),
                ('cash_returned', models.FloatField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('account', models.ForeignKey(to='core.Account')),
                ('activity', models.ForeignKey(blank=True, to='core.Activity', null=True)),
                ('budget_head', models.ForeignKey(to='core.BudgetHead')),
                ('donor', models.ForeignKey(blank=True, to='core.Donor', null=True)),
                ('receipt', models.ForeignKey(related_name='rows', to='account.Receipt')),
                ('tax_scheme', models.ForeignKey(to='core.TaxScheme')),
            ],
        ),
    ]
