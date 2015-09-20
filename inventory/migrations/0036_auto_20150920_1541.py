# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_auto_20150721_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryreportrow',
            name='entry_report',
            field=models.ForeignKey(related_name='rows', blank=True, to='inventory.EntryReport', null=True),
        ),
    ]
