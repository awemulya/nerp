# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_remove_demand_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='date',
            field=app.utils.translation.BSDateField(default='2072-2-15'),
            preserve_default=False,
        ),
    ]
