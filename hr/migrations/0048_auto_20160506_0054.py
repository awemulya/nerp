# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0047_auto_20160505_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowanceName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='IncentiveName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='allowance',
            name='description',
        ),
        migrations.RemoveField(
            model_name='allowance',
            name='name',
        ),
        migrations.RemoveField(
            model_name='incentive',
            name='description',
        ),
        migrations.RemoveField(
            model_name='incentive',
            name='name',
        ),
        migrations.AddField(
            model_name='allowance',
            name='a_name',
            field=models.ForeignKey(related_name='allowences', blank=True, to='hr.AllowanceName', null=True),
        ),
        migrations.AddField(
            model_name='incentive',
            name='i_name',
            field=models.ForeignKey(blank=True, to='hr.IncentiveName', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='allowance',
            unique_together=set([('a_name', 'employee_grade')]),
        ),
        migrations.AlterUniqueTogether(
            name='incentive',
            unique_together=set([('i_name', 'employee_grade')]),
        ),
    ]
