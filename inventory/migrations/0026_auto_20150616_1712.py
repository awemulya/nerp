# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_deprecate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Deprecate',
            new_name='Depreciation',
        ),
    ]
