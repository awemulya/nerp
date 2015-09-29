# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0039_auto_20150928_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminstance',
            name='item',
            field=models.ForeignKey(related_name='instances', to='inventory.Item'),
        ),
    ]
