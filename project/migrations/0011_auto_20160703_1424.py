# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20160701_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nprexchange',
            name='date',
            field=models.DateField(help_text=b'Date in AD'),
        ),
    ]
