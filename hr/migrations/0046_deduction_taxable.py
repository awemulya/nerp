# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0045_auto_20160502_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='taxable',
            field=models.BooleanField(default=False),
        ),
    ]
