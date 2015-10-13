# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('no', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='BudgetBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nepal_government', models.FloatField(default=0)),
                ('foreign_cash_grant', models.FloatField(default=0)),
                ('foreign_compensating_grant', models.FloatField(default=0)),
                ('foreign_cash_loan', models.FloatField(default=0)),
                ('foreign_compensating_loan', models.FloatField(default=0)),
                ('foreign_substantial_aid', models.FloatField(default=0)),
                ('nepal_government_due', models.FloatField(default=0, editable=False)),
                ('foreign_cash_grant_due', models.FloatField(default=0, editable=False)),
                ('foreign_compensating_grant_due', models.FloatField(default=0, editable=False)),
                ('foreign_cash_loan_due', models.FloatField(default=0, editable=False)),
                ('foreign_compensating_loan_due', models.FloatField(default=0, editable=False)),
                ('foreign_substantial_aid_due', models.FloatField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetHead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('no', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FiscalYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(unique=True, choices=[(2069, b'2069/70'), (2070, b'2070/71'), (2071, b'2071/72')])),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('address', models.CharField(max_length=254, null=True, blank=True)),
                ('phone_no', models.CharField(max_length=100, null=True, blank=True)),
                ('pan_no', models.CharField(max_length=50, null=True, blank=True)),
                ('account', models.OneToOneField(related_name='party', to='core.Account')),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='TaxScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('percent', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='budgetbalance',
            name='budget_head',
            field=models.ForeignKey(related_name='balance', to='core.BudgetHead'),
        ),
        migrations.AddField(
            model_name='budgetbalance',
            name='fiscal_year',
            field=models.ForeignKey(to='core.FiscalYear'),
        ),
        migrations.AlterUniqueTogether(
            name='budgetbalance',
            unique_together=set([('budget_head', 'fiscal_year')]),
        ),
    ]
