# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-25 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_auto_20170125_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporthr',
            name='allowance',
            field=models.ForeignKey(blank=True, help_text='Select if allowance amount data in this report only belogs to particular allowance.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allowance_reports', to='hr.AllowanceName'),
        ),
        migrations.AlterField(
            model_name='reporthr',
            name='deduction',
            field=models.ForeignKey(blank=True, help_text='Select if deduction amount data in this report only belongs to particular deduction.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deduction_reports', to='hr.DeductionName'),
        ),
        migrations.AlterField(
            model_name='reporthr',
            name='incentive',
            field=models.ForeignKey(blank=True, help_text='Select if incentive amount data in this report only belongs to particular incentive.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incentive_reports', to='hr.IncentiveName'),
        ),
        migrations.AlterField(
            model_name='reporthr',
            name='tax',
            field=models.ForeignKey(blank=True, help_text='Select if tax amount data in this report only belogs to particular tax deduction.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tax_reports', to='hr.TaxDeduction'),
        ),
    ]
