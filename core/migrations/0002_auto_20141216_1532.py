# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appsetting',
            name='fiscal_year',
        ),
        migrations.DeleteModel(
            name='AppSetting',
        ),
        migrations.AlterModelOptions(
            name='budgethead',
            options={},
        ),
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='budgethead',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donor',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='party',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxscheme',
            name='name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='budgethead',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='budgethead',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='taxscheme',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='taxscheme',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
