# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20151018_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationcomparison',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy]),
        ),
        migrations.AlterField(
            model_name='handover',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy]),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy]),
        ),
    ]
