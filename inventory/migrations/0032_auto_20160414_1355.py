# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 08:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0031_stockentry_stockentryrow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockentryrow',
            old_name='opening_balance',
            new_name='stock',
        ),
    ]