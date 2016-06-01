# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0098_auto_20160527_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='incentive',
            name='employee',
            field=models.ForeignKey(default=1, to='hr.Employee'),
            preserve_default=False,
        ),
    ]
