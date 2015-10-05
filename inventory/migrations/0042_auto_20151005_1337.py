# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0041_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='release_no',
            field=models.IntegerField(),
        ),
    ]
