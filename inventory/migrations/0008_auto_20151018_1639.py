# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20151018_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy]),
        ),
    ]
