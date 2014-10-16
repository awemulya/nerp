# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nepdate


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20141002_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=nepdate.BSDateField(max_length=255),
        ),
    ]
