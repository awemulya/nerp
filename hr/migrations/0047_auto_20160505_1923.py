# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0046_deduction_taxable'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowanceDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('Incentive', models.ForeignKey(related_name='allowance_amount_detail', to='hr.Allowance')),
            ],
        ),
        migrations.CreateModel(
            name='IncentiveDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('Incentive', models.ForeignKey(related_name='incentive_amount_detail', to='hr.Deduction')),
            ],
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='deduced_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='allowance_detail',
            field=models.ManyToManyField(to='hr.AllowanceDetail', blank=True),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='incentive_detail',
            field=models.ManyToManyField(to='hr.IncentiveDetail', blank=True),
        ),
    ]
