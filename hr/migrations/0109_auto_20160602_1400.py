# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0108_auto_20160529_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='amount_editable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='incentive',
            name='amount_editable',
            field=models.BooleanField(default=False),
        ),
    ]
