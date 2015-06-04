# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_item_other_properties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='other_properties',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
