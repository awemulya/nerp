# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10, choices=[(b'loan', b'Loan'), (b'grant', b'Grant')])),
                ('key', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('donor', models.ForeignKey(to='core.Donor')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetAllocationItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(null=True, blank=True)),
                ('aid', models.ForeignKey(blank=True, to='project.Aid', null=True)),
                ('budget_head', models.ForeignKey(to='core.BudgetHead')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetReleaseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(null=True, blank=True)),
                ('aid', models.ForeignKey(blank=True, to='project.Aid', null=True)),
                ('budget_head', models.ForeignKey(to='core.BudgetHead')),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(null=True, blank=True)),
                ('aid', models.ForeignKey(blank=True, to='project.Aid', null=True)),
                ('budget_head', models.ForeignKey(to='core.BudgetHead')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('enabled', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('enabled', models.BooleanField(default=True)),
                ('gon_funded', models.BooleanField(default=False, verbose_name=b'GON Funded?')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Expense Categories',
            },
        ),
        migrations.CreateModel(
            name='ExpenseRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('category', models.ForeignKey(to='project.ExpenseCategory')),
                ('expense', models.ForeignKey(to='project.Expense')),
            ],
        ),
        migrations.CreateModel(
            name='ImprestJournalVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('amount_nrs', models.FloatField(null=True, blank=True)),
                ('amount_usd', models.FloatField(null=True, blank=True)),
                ('exchange_rate', models.FloatField(null=True, blank=True)),
                ('wa_no', models.CharField(max_length=10, null=True, blank=True)),
                ('cr', models.ForeignKey(related_name='crediting_vouchers', to='account.Account')),
                ('dr', models.ForeignKey(related_name='debiting_vouchers', to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='ImprestTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, choices=[(b'initial_deposit', b'Initial Deposit'), (b'gon_fund_transfer', b'GON Fund Transfer'), (b'replenishment_received', b'Replenishment Received'), (b'payment', b'Payment'), (b'liquidation', b'Liquidation')])),
                ('date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy])),
                ('date_of_payment', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy])),
                ('wa_no', models.CharField(max_length=10, null=True, verbose_name=b'Withdrawal Application No.', blank=True)),
                ('amount_nrs', models.FloatField(null=True, blank=True)),
                ('amount_usd', models.FloatField(null=True, blank=True)),
                ('exchange_rate', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fy', models.ForeignKey(to='core.FiscalYear')),
                ('imprest_ledger', models.ForeignKey(related_name='imprest_for', to='account.Account')),
                ('initial_deposit', models.ForeignKey(related_name='deposit_for', to='account.Account')),
                ('project', models.ForeignKey(to='project.Project')),
                ('replenishments', models.ForeignKey(related_name='replenishments_for', to='account.Account')),
            ],
            options={
                'verbose_name': 'Project Fiscal Year',
                'verbose_name_plural': 'Project Fiscal Years',
            },
        ),
        migrations.CreateModel(
            name='Reimbursement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy])),
                ('bank_voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('wa_no', models.PositiveIntegerField(null=True, blank=True)),
                ('amount', models.PositiveIntegerField(null=True, blank=True)),
                ('project_fy', models.ForeignKey(to='project.ProjectFy')),
            ],
        ),
        migrations.CreateModel(
            name='Signatory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('default', models.BooleanField(default=False, verbose_name=b'Required to sign on all notes?')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name_plural': 'Signatories',
            },
        ),
        migrations.AddField(
            model_name='impresttransaction',
            name='project_fy',
            field=models.ForeignKey(to='project.ProjectFy'),
        ),
        migrations.AddField(
            model_name='imprestjournalvoucher',
            name='project_fy',
            field=models.ForeignKey(to='project.ProjectFy'),
        ),
        migrations.AddField(
            model_name='expenserow',
            name='project_fy',
            field=models.ForeignKey(to='project.ProjectFy'),
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='project',
            field=models.ForeignKey(to='project.Project'),
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ManyToManyField(to='project.ExpenseCategory', blank=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='project',
            field=models.ForeignKey(to='project.Project'),
        ),
        migrations.AddField(
            model_name='expenditure',
            name='project_fy',
            field=models.ForeignKey(to='project.ProjectFy'),
        ),
        migrations.AddField(
            model_name='budgetreleaseitem',
            name='project_fy',
            field=models.ForeignKey(to='project.ProjectFy'),
        ),
        migrations.AddField(
            model_name='budgetallocationitem',
            name='project_fy',
            field=models.ForeignKey(to='project.ProjectFy'),
        ),
        migrations.AddField(
            model_name='aid',
            name='project',
            field=models.ForeignKey(to='project.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='projectfy',
            unique_together=set([('project', 'fy')]),
        ),
    ]
