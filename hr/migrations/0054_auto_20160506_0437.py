# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0053_auto_20160506_0435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allowancedetail',
            old_name='Incentive',
            new_name='allowance',
        ),
        migrations.RenameField(
            model_name='incentivedetail',
            old_name='Incentive',
            new_name='incentive',
        ),
    ]
