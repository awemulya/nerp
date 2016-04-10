# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0023_auto_20160404_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(to='hr.Account')),
            ],
        ),
        migrations.RemoveField(
            model_name='employee',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='insurance_account',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='nalakosh_account',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='sanchayakosh_account',
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(unique=True, max_length=150, choices=[(b'bank_account', 'Bank Account'), (b'insurance_account', 'Insurance Account'), (b'nalakosh_account', 'Nagarik Lagani Kosh Account'), (b'sanchayakosh_account', 'Sanchayakosh Account')]),
        ),
        migrations.AddField(
            model_name='employeeaccount',
            name='employee',
            field=models.ForeignKey(to='hr.Employee'),
        ),
        migrations.AlterUniqueTogether(
            name='employeeaccount',
            unique_together=set([('employee', 'account')]),
        ),
    ]
