# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('current_dr', models.FloatField(null=True, blank=True)),
                ('current_cr', models.FloatField(null=True, blank=True)),
                ('tax_rate', models.FloatField(null=True, blank=True)),
                ('opening_dr', models.FloatField(default=0)),
                ('opening_cr', models.FloatField(default=0)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='account.Category', null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Journal Entries',
            },
        ),
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
                ('account', models.ForeignKey(to='account.Account')),
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
                ('account', models.ForeignKey(to='account.Account')),
                ('activity', models.ForeignKey(blank=True, to='core.Activity', null=True)),
                ('budget_head', models.ForeignKey(to='core.BudgetHead')),
                ('donor', models.ForeignKey(blank=True, to='core.Donor', null=True)),
                ('receipt', models.ForeignKey(related_name='rows', to='account.Receipt')),
                ('tax_scheme', models.ForeignKey(to='core.TaxScheme')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('current_dr', models.FloatField(null=True, blank=True)),
                ('current_cr', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(to='account.Account')),
                ('journal_entry', models.ForeignKey(related_name='transactions', to='account.JournalEntry')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='category',
            field=models.ForeignKey(related_name='accounts', blank=True, to='account.Category', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='fy',
            field=models.ForeignKey(blank=True, to='core.FiscalYear', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='account.Account', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('name', 'fy')]),
        ),
    ]
