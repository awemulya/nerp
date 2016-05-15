# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160515_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsetting',
            name='fiscal_year',
            field=models.PositiveIntegerField(default=2071, choices=[(2069, b'2069/70'), (2070, b'2070/71'), (2071, b'2071/72'), (2072, b'2072/73')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appsetting',
            name='header_for_forms',
            field=models.CharField(default=b'NERP', max_length=100),
        ),
        migrations.AddField(
            model_name='appsetting',
            name='header_for_forms_nepali',
            field=models.CharField(default='nepali', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appsetting',
            name='site_name',
            field=models.CharField(default=b'NERP', max_length=100),
        ),
    ]
