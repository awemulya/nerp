# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20160703_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imprestjournalvoucher',
            options={'ordering': ('date', 'id')},
        ),
        migrations.AlterField(
            model_name='imprestjournalvoucher',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
