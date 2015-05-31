# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_demand_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=models.DateField(),
        ),
    ]
