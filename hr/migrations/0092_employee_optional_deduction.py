# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0091_deduction_is_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='optional_deduction',
            field=models.ForeignKey(blank=True, to='hr.Deduction', null=True),
        ),
    ]
