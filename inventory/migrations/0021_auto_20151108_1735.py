# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20151108_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='fiscal_year',
        ),
        migrations.AddField(
            model_name='inspection',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy]),
        ),
    ]
