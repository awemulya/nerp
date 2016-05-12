# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0066_employee_pf_deduction_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='pf_deduction_amount',
            new_name='pf_monthly_deduction_amount',
        ),
    ]
