# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nepdate


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20141017_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=nepdate.BSDateField(max_length=255),
        ),
        migrations.AlterField(
            model_name='handover',
            name='date',
            field=nepdate.BSDateField(max_length=255),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='date',
            field=nepdate.BSDateField(max_length=255),
        ),
    ]
