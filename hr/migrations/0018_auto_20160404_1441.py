# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0017_auto_20160330_1424'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='allowence',
            new_name='allowences',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='incentive',
            new_name='incentives',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='deductions',
        ),
        migrations.AddField(
            model_name='allowence',
            name='year_allowence_cycle_month',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='incentive',
            name='year_incentive_cycle_month',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='appoint_date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dismiss_date',
            field=njango.fields.BSDateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='protempore',
            name='appoint_date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='protempore',
            name='dismiss_date',
            field=njango.fields.BSDateField(null=True, blank=True),
        ),
    ]
