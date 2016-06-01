# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_currency'),
        ('project', '0008_auto_20160507_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='expensecategory',
            options={'ordering': ('order',), 'verbose_name_plural': 'Expense Categories'},
        ),
        migrations.AddField(
            model_name='expenserow',
            name='category',
            field=models.ForeignKey(to='project.ExpenseCategory'),
        ),
        migrations.AddField(
            model_name='expenserow',
            name='expense',
            field=models.ForeignKey(to='project.Expense'),
        ),
        migrations.AddField(
            model_name='expenserow',
            name='fy',
            field=models.ForeignKey(to='core.FiscalYear'),
        ),
    ]
