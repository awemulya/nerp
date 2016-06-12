# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-05 07:52
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.manager
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_data_store'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockentry',
            options={'verbose_name_plural': 'Stock Entries'},
        ),
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='stockentry',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='stockentry',
            name='date',
            field=njango.fields.BSDateField(blank=True, default=njango.fields.today, null=True, validators=[core.models.validate_in_fy]),
        ),
    ]
