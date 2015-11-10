# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20151102_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, verbose_name='Date', validators=[core.models.validate_in_fy]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='rate',
            field=models.FloatField(null=True, verbose_name='Rate', blank=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='type',
            field=models.CharField(default=b'Waive', max_length=20, verbose_name='Type', choices=[(b'Waive', 'Waive'), (b'Handover', 'Handover'), (b'Auction', 'Auction')]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='voucher_no',
            field=models.PositiveIntegerField(verbose_name='Voucher No.'),
        ),
    ]
