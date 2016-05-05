# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0050_auto_20160506_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowance',
            name='name',
            field=models.ForeignKey(related_name='allowances', blank=True, to='hr.AllowanceName', null=True),
        ),
    ]
