# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_expensecategory_gon_funded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensecategory',
            name='gon_funded',
            field=models.BooleanField(default=False, verbose_name=b'GON Funded?'),
        ),
    ]
