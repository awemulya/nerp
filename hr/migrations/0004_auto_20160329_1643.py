# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_auto_20160328_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='allowence',
            name='duduct_type',
            field=models.CharField(default='AMOUNT', max_length=50, choices=[(b'AMOUNT', 'Amount'), (b'RATE', 'Rate')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deduction',
            name='duduct_type',
            field=models.CharField(default='AMOUNT', max_length=50, choices=[(b'AMOUNT', 'Amount'), (b'RATE', 'Rate')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incentive',
            name='duduct_type',
            field=models.CharField(default='AMOUNT', max_length=50, choices=[(b'AMOUNT', 'Amount'), (b'RATE', 'Rate')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='paid_from_date',
            field=njango.fields.BSDateField(),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='paid_to_date',
            field=njango.fields.BSDateField(),
        ),
    ]
