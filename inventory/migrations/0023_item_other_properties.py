# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_remove_inspection_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='other_properties',
            field=jsonfield.fields.JSONField(default=''),
            preserve_default=False,
        ),
    ]
