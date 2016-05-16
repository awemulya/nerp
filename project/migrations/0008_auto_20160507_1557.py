# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20160507_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.RenameModel(
            old_name='ExpenditureCategory',
            new_name='ExpenseCategory',
        ),
        migrations.RemoveField(
            model_name='expenditure',
            name='category',
        ),
        migrations.AlterModelOptions(
            name='expensecategory',
            options={'ordering': ('order',), 'verbose_name_plural': 'Expenditure Categories'},
        ),
        migrations.DeleteModel(
            name='Expenditure',
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ManyToManyField(to='project.ExpenseCategory', blank=True),
        ),
    ]
