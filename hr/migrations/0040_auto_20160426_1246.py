# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0039_auto_20160425_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeductionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('deduction', models.ForeignKey(related_name='deduced_amount_detail', to='hr.Deduction')),
            ],
        ),
        migrations.RemoveField(
            model_name='paymentrecord',
            name='deduced_amount',
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='deduction_detail',
            field=models.ManyToManyField(to='hr.DeductionDetail', blank=True),
        ),
    ]
