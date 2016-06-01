# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0090_auto_20160526_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='is_optional',
            field=models.BooleanField(default=False),
        ),
    ]
