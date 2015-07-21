# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0032_release'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demandrow',
            name='release_quantity',
        ),
    ]
