# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inspection_inspectionrow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspectionrow',
            name='transaction',
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='account_no',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='item_name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='price',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='property_classification_reference_number',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='quantity',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='rate',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inspectionrow',
            name='unit',
            field=models.CharField(default='pieces', max_length=50),
            preserve_default=True,
        ),
    ]
