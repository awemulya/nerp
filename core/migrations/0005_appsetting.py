# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151104_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(default=b'NERP', max_length=100)),
                ('fiscal_year', models.CharField(max_length=100, choices=[(2069, b'2069/70'), (2070, b'2070/71'), (2071, b'2071/72'), (2072, b'2072/73')])),
                ('header_for_forms', models.CharField(default=b'NERP', max_length=100)),
                ('header_for_forms_nepali', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
