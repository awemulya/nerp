# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20160630_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disbursementdetail',
            name='party',
            field=models.ForeignKey(blank=True, to='account.Party', null=True),
        ),
    ]
