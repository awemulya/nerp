# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0051_auto_20160506_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incentive',
            name='name',
            field=models.ForeignKey(related_name='incentives', blank=True, to='hr.IncentiveName', null=True),
        ),
    ]
