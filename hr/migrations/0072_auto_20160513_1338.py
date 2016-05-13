# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0071_auto_20160513_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxscheme',
            name='is_last',
        ),
        migrations.AddField(
            model_name='taxscheme',
            name='priority',
            field=models.PositiveIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
