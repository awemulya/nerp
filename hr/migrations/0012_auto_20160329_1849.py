# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0011_auto_20160329_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deduction',
            old_name='duduct_type',
            new_name='deduct_type',
        ),
    ]
