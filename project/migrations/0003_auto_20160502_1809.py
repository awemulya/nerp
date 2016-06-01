# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20160502_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impresttransaction',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy]),
        ),
    ]
