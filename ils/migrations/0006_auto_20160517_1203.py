# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-17 06:18
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0005_merge'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='subject',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
