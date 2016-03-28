# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrecord',
            name='deduction',
        ),
        migrations.AddField(
            model_name='employee',
            name='deductions',
            field=models.ManyToManyField(to='hr.Deduction'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='deduced_amount',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
