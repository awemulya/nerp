# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0015_deduction_deduction_for_dm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='deduction_for',
            field=models.CharField(max_length=50, choices=[(b'EMPLOYEE ACC', 'For employee Account'), (b'EXPLICIT ACC', 'An Explicit Account')]),
        ),
    ]
