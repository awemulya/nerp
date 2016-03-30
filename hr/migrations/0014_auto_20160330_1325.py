# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0013_auto_20160330_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deduction',
            old_name='deducttion_for',
            new_name='deduction_for',
        ),
    ]
