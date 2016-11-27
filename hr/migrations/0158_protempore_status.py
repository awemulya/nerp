# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-25 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0157_auto_20161125_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='protempore',
            name='status',
            field=models.CharField(choices=[(b'STARTED', 'Started'), (b'ENDED', 'ENDED'), (b'READY_FOR_PAYMENT', 'Ready for Payment'), (b'PAID', 'Paid')], default=b'STARTED', max_length=128),
        ),
    ]