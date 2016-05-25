# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20160502_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impresttransaction',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='impresttransaction',
            name='currency',
        ),
        migrations.AddField(
            model_name='impresttransaction',
            name='amount_nrs',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='impresttransaction',
            name='amount_usd',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
