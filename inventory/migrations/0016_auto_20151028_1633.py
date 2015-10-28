# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20151028_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminstance',
            name='location',
            field=models.ForeignKey(to='inventory.ItemLocation', null=True),
        ),
    ]
