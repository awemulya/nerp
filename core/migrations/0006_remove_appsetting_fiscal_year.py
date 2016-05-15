# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_appsetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appsetting',
            name='fiscal_year',
        ),
    ]
