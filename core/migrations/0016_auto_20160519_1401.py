# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160519_1401'),
        ('project', '0022_auto_20160519_1401'),
        ('core', '0015_auto_20160518_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='party',
            name='account',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
