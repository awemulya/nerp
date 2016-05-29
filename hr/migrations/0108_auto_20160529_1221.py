# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0107_deduction_permanent_multiply_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='optional_deduction',
            new_name='optional_deductions',
        ),
    ]
