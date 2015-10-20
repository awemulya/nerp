# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20151019_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instancehistory',
            name='to_user',
            field=models.ForeignKey(related_name='to_history', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
