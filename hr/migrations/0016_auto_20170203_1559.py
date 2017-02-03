# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-03 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0015_auto_20170131_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporthr',
            name='allowance',
        ),
        migrations.AddField(
            model_name='reporthr',
            name='allowance',
            field=models.ManyToManyField(blank=True, help_text='Select if allowance amount data in this report only belogs to particular allowance.', null=True, related_name='allowance_reports', to='hr.AllowanceName'),
        ),
        migrations.RemoveField(
            model_name='reporthr',
            name='deduction',
        ),
        migrations.AddField(
            model_name='reporthr',
            name='deduction',
            field=models.ManyToManyField(blank=True, help_text='Select if deduction amount data in this report only belongs to particular deduction.', null=True, related_name='deduction_reports', to='hr.DeductionName'),
        ),
        migrations.RemoveField(
            model_name='reporthr',
            name='incentive',
        ),
        migrations.AddField(
            model_name='reporthr',
            name='incentive',
            field=models.ManyToManyField(blank=True, help_text='Select if incentive amount data in this report only belongs to particular incentive.', null=True, related_name='incentive_reports', to='hr.IncentiveName'),
        ),
        migrations.RemoveField(
            model_name='reporthr',
            name='tax',
        ),
        migrations.AddField(
            model_name='reporthr',
            name='tax',
            field=models.ManyToManyField(blank=True, help_text='Select if tax amount data in this report only belogs to particular tax deduction.', null=True, related_name='tax_reports', to='hr.TaxDeduction'),
        ),
    ]
