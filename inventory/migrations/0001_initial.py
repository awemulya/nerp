# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.translation
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('core', '0002_auto_20141216_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=254, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='inventory.Category', null=True)),
            ],
            options={
                'verbose_name_plural': 'Inventory Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_no', models.IntegerField(null=True, blank=True)),
                ('date', app.utils.translation.BSDateField()),
                ('purpose', models.CharField(max_length=254)),
                ('demandee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DemandRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=254, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
                ('release_quantity', models.FloatField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('status', models.CharField(default=b'Requested', max_length=9, choices=[(b'Requested', b'Requested'), (b'Approved', b'Approved'), (b'Fulfilled', b'Fulfilled')])),
                ('demand', models.ForeignKey(related_name=b'rows', to='inventory.Demand')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_report_no', models.PositiveIntegerField(null=True, blank=True)),
                ('source_object_id', models.PositiveIntegerField()),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
                ('source_content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryReportRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=254, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
                ('rate', models.FloatField()),
                ('other_expenses', models.FloatField(default=0)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('entry_report', models.ForeignKey(related_name=b'rows', to='inventory.EntryReport')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Handover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('addressee', models.CharField(max_length=254)),
                ('date', app.utils.translation.BSDateField()),
                ('office', models.CharField(max_length=254)),
                ('designation', models.CharField(max_length=254)),
                ('handed_to', models.CharField(max_length=254)),
                ('due_days', models.PositiveIntegerField(default=7)),
                ('type', models.CharField(default=b'Incoming', max_length=9, choices=[(b'Incoming', b'Incoming'), (b'Outgoing', b'Outgoing')])),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HandoverRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=254, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
                ('total_amount', models.FloatField()),
                ('received_date', models.DateField(null=True, blank=True)),
                ('condition', models.TextField(null=True, blank=True)),
                ('handover', models.ForeignKey(related_name=b'rows', to='inventory.Handover')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventoryAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('account_no', models.PositiveIntegerField()),
                ('current_balance', models.FloatField(default=0)),
                ('opening_balance', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InventoryAccountRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_of_production_or_company_name', models.CharField(max_length=254, null=True, blank=True)),
                ('size', models.CharField(max_length=254, null=True, blank=True)),
                ('expected_life', models.CharField(max_length=254, null=True, blank=True)),
                ('source', models.CharField(max_length=254, null=True, blank=True)),
                ('expense_total_cost_price', models.FloatField(null=True, blank=True)),
                ('remaining_total_cost_price', models.FloatField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.CharField(default=b'consumable', max_length=15, choices=[(b'consumable', 'Consumable'), (b'non-consumable', 'Non-Consumable')])),
                ('unit', models.CharField(default='pieces', max_length=50)),
                ('property_classification_reference_number', models.CharField(max_length=20, null=True, blank=True)),
                ('account', models.OneToOneField(related_name=b'item', null=True, to='inventory.InventoryAccount')),
                ('category', models.ForeignKey(blank=True, to='inventory.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', app.utils.translation.BSDateField()),
                ('model_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name=b'inventory_journal_entries', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'InventoryJournal Entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_no', models.IntegerField(null=True, blank=True)),
                ('date', app.utils.translation.BSDateField()),
                ('due_days', models.IntegerField(default=3)),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
                ('party', models.ForeignKey(to='core.Party')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseOrderRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('budget_title_no', models.IntegerField(null=True, blank=True)),
                ('specification', models.CharField(max_length=254, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
                ('rate', models.FloatField()),
                ('vattable', models.BooleanField(default=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('item', models.ForeignKey(to='inventory.Item')),
                ('purchase_order', models.ForeignKey(related_name=b'rows', to='inventory.PurchaseOrder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('current_balance', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(to='inventory.InventoryAccount')),
                ('journal_entry', models.ForeignKey(related_name=b'transactions', to='inventory.JournalEntry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inventoryaccountrow',
            name='journal_entry',
            field=models.OneToOneField(related_name=b'account_row', to='inventory.JournalEntry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='handoverrow',
            name='item',
            field=models.ForeignKey(to='inventory.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entryreportrow',
            name='item',
            field=models.ForeignKey(to='inventory.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='demandrow',
            name='item',
            field=models.ForeignKey(to='inventory.Item'),
            preserve_default=True,
        ),
    ]
