# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-24 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0022_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
    ]