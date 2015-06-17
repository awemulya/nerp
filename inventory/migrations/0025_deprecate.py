# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_auto_20150603_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deprecate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('depreciate_type', models.CharField(default=b'Fixed percentage', max_length=25, choices=[(b'Fixed percentage', 'Fixed percentage'), (b'Compounded percentage', 'Compounded percentage'), (b'Fixed price', 'Fixed price')])),
                ('depreciate_value', models.PositiveIntegerField(default=0)),
                ('time', models.PositiveIntegerField(default=0)),
                ('time_type', models.CharField(default=b'Year', max_length=5, choices=[(b'Day', 'Day'), (b'Month', 'Month'), (b'Year', 'Year')])),
            ],
        ),
    ]
