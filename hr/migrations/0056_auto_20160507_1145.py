# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0055_payrollentry_transacted'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollentry',
            name='branch',
            field=models.ForeignKey(blank=True, to='hr.BranchOffice', null=True),
        ),
        migrations.AddField(
            model_name='payrollentry',
            name='is_monthly_payroll',
            field=models.BooleanField(default=False),
        ),
    ]
