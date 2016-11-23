# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-22 10:20
from __future__ import unicode_literals

import datetime
from django.db import migrations
from django.utils.timezone import utc
import hr.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0151_auto_20161121_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollentry',
            name='paid_from_date',
            field=hr.fields.HRBSDateField(default=datetime.datetime(2016, 11, 22, 10, 20, 34, 4020, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payrollentry',
            name='paid_to_date',
            field=hr.fields.HRBSDateField(default=datetime.datetime(2016, 11, 22, 10, 20, 46, 756520, tzinfo=utc)),
            preserve_default=False,
        ),
    ]