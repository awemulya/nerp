# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
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
            name='InspectionRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('matched_number', models.PositiveIntegerField(null=True, blank=True)),
                ('unmatched_number', models.PositiveIntegerField(null=True, blank=True)),
                ('decrement', models.PositiveIntegerField(null=True, blank=True)),
                ('increment', models.PositiveIntegerField(null=True, blank=True)),
                ('decrement_increment_price', models.FloatField(null=True, blank=True)),
                ('in_condition', models.PositiveIntegerField(null=True, blank=True)),
                ('not_in_condition', models.PositiveIntegerField(null=True, blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('inspection', models.ForeignKey(related_name='rows', to='inventory.Inspection')),
                ('transaction', models.ForeignKey(to='inventory.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
