# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0041_payrollentry_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='with_temporary_employee',
            field=models.BooleanField(default=False),
        ),
    ]
