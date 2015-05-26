# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20150525_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=app.utils.translation.BSDateField(),
        ),
    ]
