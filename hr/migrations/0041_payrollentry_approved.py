# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0040_auto_20160426_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollentry',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
