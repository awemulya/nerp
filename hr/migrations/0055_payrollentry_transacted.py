# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0054_auto_20160506_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollentry',
            name='transacted',
            field=models.BooleanField(default=False),
        ),
    ]
