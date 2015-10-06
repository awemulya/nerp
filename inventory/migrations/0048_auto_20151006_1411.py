# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0047_auto_20151006_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='report_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
