# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0042_deduction_with_temporary_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='add2_init_salary',
            field=models.BooleanField(default=False),
        ),
    ]
