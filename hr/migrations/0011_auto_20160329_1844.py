# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_auto_20160329_1835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allowence',
            old_name='duduct_type',
            new_name='sum_type',
        ),
        migrations.RenameField(
            model_name='incentive',
            old_name='duduct_type',
            new_name='sum_type',
        ),
    ]
