# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impresttransaction',
            name='date',
            field=njango.fields.BSDateField(default=datetime.date.today, null=True, blank=True),
        ),
    ]
