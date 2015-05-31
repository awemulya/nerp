# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20150525_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='transaction',
            field=models.ForeignKey(related_name='inspection', default='', to='inventory.Transaction'),
            preserve_default=False,
        ),
    ]
