# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_inspection_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='transaction',
        ),
    ]
