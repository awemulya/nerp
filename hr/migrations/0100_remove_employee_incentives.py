# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0099_incentive_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='incentives',
        ),
    ]
