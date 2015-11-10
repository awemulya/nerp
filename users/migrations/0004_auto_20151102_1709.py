# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151020_1453'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupproxy',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
    ]
