# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0044_employee_marital_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(default=b'U', max_length=1, choices=[(b'M', 'Married'), (b'U', 'Unmarried')]),
        ),
    ]
