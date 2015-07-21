# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0034_remove_release_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='demand_row',
            field=models.ForeignKey(related_name='releases', to='inventory.DemandRow'),
        ),
    ]
