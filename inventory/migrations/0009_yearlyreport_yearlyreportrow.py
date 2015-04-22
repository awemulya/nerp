# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('inventory', '0008_auto_20150422_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearlyReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_no', models.IntegerField(null=True, blank=True)),
                ('fiscal_year', models.ForeignKey(to='core.FiscalYear')),
            ],
            options={
            },
            bases=(models.Model,),
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
            options={
            },
            bases=(models.Model,),
        ),
    ]
