# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150419_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspectionrow',
            name='in_condition',
        ),
        migrations.RemoveField(
            model_name='inspectionrow',
            name='not_in_condition',
        ),
    ]
