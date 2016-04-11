# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0027_auto_20160410_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='account_holder_type',
        ),
        migrations.RemoveField(
            model_name='account',
            name='account_type',
        ),
        migrations.AddField(
            model_name='employeeaccount',
            name='account_type',
            field=models.ForeignKey(to='hr.AccountType', null=True),
        ),
        migrations.AlterField(
            model_name='employeeaccount',
            name='account',
            field=models.OneToOneField(related_name='employee_account', to='hr.Account'),
        ),
        migrations.AddField(
            model_name='companyaccount',
            name='account',
            field=models.OneToOneField(related_name='company_account', to='hr.Account'),
        ),
    ]
