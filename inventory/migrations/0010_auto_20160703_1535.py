# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-03 09:50
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20160703_1424'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
