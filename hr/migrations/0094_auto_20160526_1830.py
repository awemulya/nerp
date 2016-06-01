# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0093_auto_20160526_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='optional_deduction',
        ),
        migrations.AddField(
            model_name='employee',
            name='optional_deduction',
            field=models.ManyToManyField(to='hr.Deduction'),
        ),
    ]
