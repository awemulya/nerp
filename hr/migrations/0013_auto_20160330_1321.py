# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0012_auto_20160329_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='deducttion_for',
            field=models.CharField(max_length=50, null=True, choices=[(b'EMPLOYEE ACC', 'For employee Account'), (b'EXPLICIT ACC', 'An Explicit Account')]),
        ),
        migrations.AddField(
            model_name='deduction',
            name='explicit_acc',
            field=models.ForeignKey(to='hr.Account', null=True),
        ),
    ]
