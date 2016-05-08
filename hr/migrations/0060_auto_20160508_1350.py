# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0059_companyaccount_is_salary_giving'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowanceAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(related_name='allowance_ledger', to='hr.Account')),
            ],
        ),
        migrations.CreateModel(
            name='DeductionAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(related_name='deduction_ledger', to='hr.Account')),
            ],
        ),
        migrations.CreateModel(
            name='IncentiveAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(related_name='incentive_ledger', to='hr.Account')),
            ],
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='allowance_detail',
            new_name='allowance_details',
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='deduction_detail',
            new_name='deduction_details',
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='incentive_detail',
            new_name='incentive_details',
        ),
        migrations.RenameField(
            model_name='payrollentry',
            old_name='entry_row',
            new_name='entry_rows',
        ),
    ]
