# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20160507_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expenditure',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='expenditure',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
