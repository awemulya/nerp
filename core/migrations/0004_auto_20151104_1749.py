# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151018_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='name',
            field=models.CharField(max_length=254, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='party',
            name='name_en',
            field=models.CharField(max_length=254, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='party',
            name='name_ne',
            field=models.CharField(max_length=254, null=True, verbose_name='Name'),
        ),
    ]
