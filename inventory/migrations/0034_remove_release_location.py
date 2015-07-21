# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0033_remove_demandrow_release_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='release',
            name='location',
        ),
    ]
