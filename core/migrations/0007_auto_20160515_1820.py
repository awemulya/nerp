# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_appsetting_fiscal_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appsetting',
            name='header_for_forms',
        ),
        migrations.RemoveField(
            model_name='appsetting',
            name='header_for_forms_nepali',
        ),
        migrations.RemoveField(
            model_name='appsetting',
            name='site_name',
        ),
    ]
