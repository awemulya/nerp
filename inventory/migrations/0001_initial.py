# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import core.models
import njango.fields
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
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
            ],
            options={
                'verbose_name_plural': 'Inventory Categories',
            },
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('purpose', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='DemandRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=254, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('status', models.CharField(default=b'Requested', max_length=9, choices=[(b'Requested', 'Requested'), (b'Approved', 'Approved'), (b'Fulfilled', 'Fulfilled')])),
                ('purpose', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Depreciation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('depreciate_type', models.CharField(default=b'Fixed percentage', max_length=25, choices=[(b'Fixed percentage', 'Fixed percentage'), (b'Fixed price', 'Fixed price')])),
                ('depreciate_value', models.FloatField(default=0)),
                ('time', models.FloatField(default=0)),
                ('time_type', models.CharField(default=b'years', max_length=8, choices=[(b'days', 'Day(s)'), (b'months', 'Month(s)'), (b'years', 'Year(s)')])),
            ],
        ),
        migrations.CreateModel(
            name='EntryReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_report_no', models.PositiveIntegerField(null=True, blank=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('source_object_id', models.PositiveIntegerField()),
            ],
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
                ('vattable', models.BooleanField(default=True)),
                ('other_expenses', models.FloatField(default=0)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(verbose_name='Voucher No.')),
                ('date', njango.fields.BSDateField(default=njango.fields.today, verbose_name='Date', validators=[core.models.validate_in_fy])),
                ('type', models.CharField(default=b'Waive', max_length=20, verbose_name='Type', choices=[(b'Waive', 'Waive'), (b'Handover', 'Handover'), (b'Auction', 'Auction')])),
                ('rate', models.FloatField(null=True, verbose_name='Rate', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Handover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('addressee', models.CharField(max_length=254)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('office', models.CharField(max_length=254)),
                ('designation', models.CharField(max_length=254)),
                ('handed_to', models.CharField(max_length=254)),
                ('due_days', models.PositiveIntegerField(default=7)),
                ('type', models.CharField(default=b'Incoming', max_length=9, choices=[(b'Incoming', b'Incoming'), (b'Outgoing', b'Outgoing')])),
            ],
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
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
            ],
        ),
        migrations.CreateModel(
            name='InspectionRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('account_no', models.PositiveIntegerField()),
                ('property_classification_reference_number', models.CharField(max_length=20, null=True, blank=True)),
                ('item_name', models.CharField(max_length=254)),
                ('unit', models.CharField(default='pieces', max_length=50)),
                ('quantity', models.FloatField()),
                ('rate', models.FloatField()),
                ('price', models.FloatField(null=True, blank=True)),
                ('matched_number', models.PositiveIntegerField(null=True, blank=True)),
                ('unmatched_number', models.PositiveIntegerField(null=True, blank=True)),
                ('decrement', models.PositiveIntegerField(null=True, blank=True)),
                ('increment', models.PositiveIntegerField(null=True, blank=True)),
                ('decrement_increment_price', models.FloatField(null=True, blank=True)),
                ('good', models.PositiveIntegerField(null=True, blank=True)),
                ('bad', models.PositiveIntegerField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstanceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, verbose_name='Date', validators=[core.models.validate_in_fy])),
            ],
            options={
                'verbose_name_plural': 'Instance History',
            },
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
                ('opening_rate', models.FloatField(default=0)),
                ('opening_rate_vattable', models.BooleanField(default=True)),
            ],
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
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.CharField(default=b'consumable', max_length=15, choices=[(b'consumable', 'Consumable'), (b'non-consumable', 'Non-consumable')])),
                ('unit', models.CharField(default='pieces', max_length=50)),
                ('property_classification_reference_number', models.CharField(max_length=20, null=True, blank=True)),
                ('other_properties', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_rate', models.FloatField(null=True)),
                ('other_properties', jsonfield.fields.JSONField(null=True, blank=True)),
                ('item', models.ForeignKey(related_name='instances', to='inventory.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField()),
                ('model_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name='inventory_journal_entries', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'InventoryJournal Entries',
            },
        ),
        migrations.CreateModel(
            name='PartyQuotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('per_unit_price', models.FloatField()),
                ('party', models.ForeignKey(related_name='party_quote', to='core.Party')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_no', models.IntegerField(null=True, blank=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('due_days', models.IntegerField(default=3)),
                ('party', models.ForeignKey(to='core.Party')),
            ],
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
                ('purchase_order', inventory.models.UnsavedForeignKey(related_name='rows', to='inventory.PurchaseOrder')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationComparison',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy])),
            ],
        ),
        migrations.CreateModel(
            name='QuotationComparisonRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=250, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('estimated_cost', models.FloatField()),
                ('item', models.ForeignKey(related_name='item_quotation', to='inventory.Item')),
                ('quotation', models.ForeignKey(related_name='rows', to='inventory.QuotationComparison')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('demand_row', models.ForeignKey(related_name='releases', to='inventory.DemandRow')),
                ('item_instance', models.ForeignKey(to='inventory.ItemInstance')),
                ('location', models.ForeignKey(to='inventory.ItemLocation')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('head_office', models.BooleanField(default=False)),
                ('branch_office', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(verbose_name='Voucher No.')),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
            ],
        ),
        migrations.CreateModel(
            name='StockEntryRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(null=True, blank=True)),
                ('unit', models.CharField(default='pieces', max_length=50)),
                ('account_no', models.PositiveIntegerField()),
                ('opening_stock', models.FloatField(default=0, null=True, blank=True)),
                ('opening_rate', models.FloatField(default=0, null=True, blank=True)),
                ('opening_rate_vattable', models.BooleanField(default=True)),
                ('item', models.OneToOneField(null=True, blank=True, to='inventory.Item')),
                ('stock_entry', inventory.models.UnsavedForeignKey(related_name='rows', to='inventory.StockEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('current_balance', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(to='inventory.InventoryAccount')),
                ('journal_entry', models.ForeignKey(related_name='transactions', to='inventory.JournalEntry')),
            ],
        ),
        migrations.CreateModel(
            name='YearlyReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fiscal_year', models.OneToOneField(to='core.FiscalYear')),
            ],
        ),
        migrations.CreateModel(
            name='YearlyReportRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('account_no', models.PositiveIntegerField()),
                ('property_classification_reference_number', models.CharField(max_length=20, null=True, blank=True)),
                ('item_name', models.CharField(max_length=254)),
                ('income', models.FloatField()),
                ('expense', models.FloatField()),
                ('remaining', models.FloatField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('yearly_report', models.ForeignKey(related_name='rows', to='inventory.YearlyReport')),
            ],
        ),
        migrations.AddField(
            model_name='partyquotation',
            name='quotation_comparison_row',
            field=models.ForeignKey(related_name='bidder_quote', blank=True, to='inventory.QuotationComparisonRow', null=True),
        ),
        migrations.AddField(
            model_name='iteminstance',
            name='location',
            field=models.ForeignKey(to='inventory.ItemLocation', null=True),
        ),
        migrations.AddField(
            model_name='iteminstance',
            name='source',
            field=models.ForeignKey(blank=True, to='inventory.EntryReportRow', null=True),
        ),
    ]
