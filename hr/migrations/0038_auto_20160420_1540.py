# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0037_paymentrecord_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allowance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('sum_type', models.CharField(max_length=50, choices=[(b'AMOUNT', 'Amount'), (b'RATE', 'Rate')])),
                ('amount', models.FloatField(null=True, blank=True)),
                ('amount_rate', models.FloatField(null=True, blank=True)),
                ('payment_cycle', models.CharField(max_length=50, choices=[(b'M', 'Monthly'), (b'Y', 'Yearly'), (b'D', 'Daily'), (b'H', 'Hourly')])),
                ('year_payment_cycle_month', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('description', models.CharField(max_length=250)),
                ('employee_grade', models.ForeignKey(to='hr.EmployeeGrade')),
            ],
        ),
        migrations.RemoveField(
            model_name='allowence',
            name='employee_grade',
        ),
        migrations.RenameField(
            model_name='paymentrecord',
            old_name='allowence',
            new_name='allowance',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='allowences',
        ),
        migrations.DeleteModel(
            name='Allowence',
        ),
        migrations.AddField(
            model_name='employee',
            name='allowances',
            field=models.ManyToManyField(to='hr.Allowance', blank=True),
        ),
    ]
