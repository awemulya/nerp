# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-25 12:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0158_protempore_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protempore',
            name='paid',
        ),
    ]