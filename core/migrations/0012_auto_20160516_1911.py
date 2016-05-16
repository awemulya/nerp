# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20160516_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsetting',
            name='header_for_forms',
            field=models.TextField(default=b'NERP'),
        ),
        migrations.AlterField(
            model_name='appsetting',
            name='header_for_forms_nepali',
            field=models.TextField(default=b'NERP'),
        ),
    ]
