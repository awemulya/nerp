# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151104_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
                ('latest_usd_rate', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
    ]
