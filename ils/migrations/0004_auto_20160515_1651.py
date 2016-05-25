# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0003_auto_20160224_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibrarySetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fine_per_day', models.FloatField(default=2)),
                ('borrow_days', models.PositiveIntegerField(default=7)),
                ('default_type', models.CharField(default=b'Circulative', max_length=50, choices=[(b'Reference', b'Reference'), (b'Circulative', b'Circulative')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelManagers(
            name='subject',
            managers=[
            ],
        ),
    ]
