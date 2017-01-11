# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160630_1205'),
        ('project', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='disbursementdetail',
            name='category',
            field=models.ForeignKey(default=None, to='project.ExpenseCategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disbursementdetail',
            name='party',
            field=models.ForeignKey(default=None, to='account.Party'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disbursementdetail',
            name='response_nrs',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='disbursementdetail',
            name='response_sdr',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='disbursementdetail',
            name='response_usd',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='disbursementdetail',
            name='value_date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy]),
        ),
        migrations.AlterField(
            model_name='disbursementdetail',
            name='remarks',
            field=models.TextField(null=True, blank=True),
        ),
    ]
