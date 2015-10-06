# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0038_auto_20150920_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='handover',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
