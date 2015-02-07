# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.flexible_date


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0005_auto_20150207_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='date_of_publication',
        ),
        migrations.AddField(
            model_name='record',
            name='publication_date',
            field=app.utils.flexible_date.FlexibleDateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
