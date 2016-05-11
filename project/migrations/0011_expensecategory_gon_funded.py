# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20160511_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensecategory',
            name='gon_funded',
            field=models.BooleanField(default=False),
        ),
    ]
