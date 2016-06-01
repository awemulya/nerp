# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0087_auto_20160526_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deduction',
            name='account',
        ),
        migrations.RemoveField(
            model_name='deduction',
            name='deduction_for',
        ),
        migrations.RemoveField(
            model_name='deduction',
            name='explicit_acc',
        ),
        migrations.RemoveField(
            model_name='deduction',
            name='in_acc_type',
        ),
    ]
