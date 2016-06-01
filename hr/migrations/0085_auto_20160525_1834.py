# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0084_salaryaccount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalentry',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='account',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='journal_entry',
        ),
        migrations.AlterField(
            model_name='allowanceaccount',
            name='account',
            field=models.OneToOneField(related_name='allowance_ledger', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='companyaccount',
            name='account',
            field=models.OneToOneField(related_name='company_account', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='deduction',
            name='explicit_acc',
            field=models.ForeignKey(blank=True, to='account.Account', null=True),
        ),
        migrations.AlterField(
            model_name='deductionaccount',
            name='account',
            field=models.OneToOneField(related_name='deduction_ledger', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='accounts',
            field=models.ManyToManyField(to='account.Account', through='hr.EmployeeAccount'),
        ),
        migrations.AlterField(
            model_name='employeeaccount',
            name='account',
            field=models.OneToOneField(related_name='employee_account', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='incentiveaccount',
            name='account',
            field=models.OneToOneField(related_name='incentive_ledger', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='salaryaccount',
            name='account',
            field=models.OneToOneField(related_name='salary_account', to='account.Account'),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='JournalEntry',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
