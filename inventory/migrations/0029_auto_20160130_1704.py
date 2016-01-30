# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_auto_20151126_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='entryreport',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy]),
        ),
        migrations.AlterField(
            model_name='depreciation',
            name='depreciate_type',
            field=models.CharField(default=b'Fixed percentage', max_length=25, choices=[(b'Fixed percentage', 'Fixed percentage'), (b'Fixed price', 'Fixed price')]),
        ),
    ]
