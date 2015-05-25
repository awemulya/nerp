# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_auto_20150524_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='date',
        ),
    ]
