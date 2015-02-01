# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0003_record_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='excerpt',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
