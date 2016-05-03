# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20160502_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impresttransaction',
            name='description',
        ),
        migrations.RemoveField(
            model_name='impresttransaction',
            name='ref',
        ),
        migrations.AddField(
            model_name='impresttransaction',
            name='date_of_payment',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True, validators=[core.models.validate_in_fy]),
        ),
    ]
