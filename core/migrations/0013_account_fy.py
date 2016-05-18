# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160516_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fy',
            field=models.ForeignKey(blank=True, to='core.FiscalYear', null=True),
        ),
    ]
