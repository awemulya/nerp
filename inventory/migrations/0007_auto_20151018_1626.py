# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_inventoryaccount_opening_rate_vattable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='demandee',
            field=models.ForeignKey(related_name='demands', to=settings.AUTH_USER_MODEL),
        ),
    ]
