# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.flexible_date


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0006_auto_20150207_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='publication_date',
        ),
        migrations.AddField(
            model_name='record',
            name='date_of_publication',
            field=app.utils.flexible_date.FlexibleDateField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
