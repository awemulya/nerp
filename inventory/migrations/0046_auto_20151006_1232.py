# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0045_auto_20151005_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminstance',
            name='location',
            field=models.ForeignKey(related_name='item_instance', to='inventory.ItemLocation'),
        ),
    ]
