# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0043_deduction_add2_init_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(default=b'U', max_length=1),
        ),
    ]
