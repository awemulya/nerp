# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0089_deduction_deduct_in_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='deduct_in_category',
            field=models.ForeignKey(default=1, blank=True, to='account.Category'),
            preserve_default=False,
        ),
    ]
