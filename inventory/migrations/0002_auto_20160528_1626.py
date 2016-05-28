# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='iteminstance',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='account',
            field=models.OneToOneField(related_name='item', null=True, to='inventory.InventoryAccount'),
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, to='inventory.Category', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='depreciation',
            field=models.ForeignKey(related_name='depreciate_item', blank=True, to='inventory.Depreciation', null=True),
        ),
        migrations.AddField(
            model_name='inventoryaccountrow',
            name='journal_entry',
            field=models.OneToOneField(related_name='account_row', to='inventory.JournalEntry'),
        ),
        migrations.AddField(
            model_name='instancehistory',
            name='from_location',
            field=models.ForeignKey(related_name='from_history', verbose_name='From Location', to='inventory.ItemLocation'),
        ),
        migrations.AddField(
            model_name='instancehistory',
            name='from_user',
            field=models.ForeignKey(related_name='from_history', verbose_name='From User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='instancehistory',
            name='instance',
            field=models.ForeignKey(to='inventory.ItemInstance'),
        ),
        migrations.AddField(
            model_name='instancehistory',
            name='to_location',
            field=models.ForeignKey(related_name='to_history', verbose_name='To Location', to='inventory.ItemLocation', null=True),
        ),
        migrations.AddField(
            model_name='instancehistory',
            name='to_user',
            field=models.ForeignKey(related_name='to_history', verbose_name='To User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='inspection',
            field=models.ForeignKey(related_name='rows', to='inventory.Inspection'),
        ),
        migrations.AddField(
            model_name='handoverrow',
            name='handover',
            field=models.ForeignKey(related_name='rows', to='inventory.Handover'),
        ),
        migrations.AddField(
            model_name='handoverrow',
            name='item',
            field=models.ForeignKey(to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='expense',
            name='instance',
            field=models.ForeignKey(to='inventory.ItemInstance'),
        ),
        migrations.AddField(
            model_name='entryreportrow',
            name='entry_report',
            field=models.ForeignKey(related_name='rows', blank=True, to='inventory.EntryReport', null=True),
        ),
        migrations.AddField(
            model_name='entryreportrow',
            name='item',
            field=models.ForeignKey(to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='entryreport',
            name='source_content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='demandrow',
            name='demand',
            field=models.ForeignKey(related_name='rows', to='inventory.Demand'),
        ),
        migrations.AddField(
            model_name='demandrow',
            name='item',
            field=models.ForeignKey(to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='demandrow',
            name='location',
            field=models.ForeignKey(blank=True, to='inventory.ItemLocation', null=True),
        ),
        migrations.AddField(
            model_name='demand',
            name='demandee',
            field=models.ForeignKey(related_name='demands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='inventory.Category', null=True),
        ),
    ]
