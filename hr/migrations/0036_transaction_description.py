# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0035_paymentrecord_pro_tempore_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='transaction description default value', max_length=120),
            preserve_default=False,
        ),
    ]
