# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-03 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0016_auto_20170203_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporthr',
            name='allowance',
            field=models.ManyToManyField(blank=True, help_text='Select if allowance amount data in this report only belogs to particular allowance.', related_name='allowance_reports', to='hr.AllowanceName'),
        ),
        migrations.AlterField(
            model_name='reporthr',
            name='deduction',
            field=models.ManyToManyField(blank=True, help_text='Select if deduction amount data in this report only belongs to particular deduction.', related_name='deduction_reports', to='hr.DeductionName'),
        ),
        migrations.AlterField(
            model_name='reporthr',
            name='incentive',
            field=models.ManyToManyField(blank=True, help_text='Select if incentive amount data in this report only belongs to particular incentive.', related_name='incentive_reports', to='hr.IncentiveName'),
        ),
        migrations.AlterField(
            model_name='reporthr',
            name='tax',
            field=models.ManyToManyField(blank=True, help_text='Select if tax amount data in this report only belogs to particular tax deduction.', related_name='tax_reports', to='hr.TaxDeduction'),
        ),
    ]