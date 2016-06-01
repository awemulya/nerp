# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0092_employee_optional_deduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='deduct_in_category',
            field=models.ForeignKey(blank=True, to='account.Category', null=True),
        ),
    ]
