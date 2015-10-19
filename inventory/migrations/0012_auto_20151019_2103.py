# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_instancehistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instancehistory',
            options={'verbose_name_plural': 'Instance History'},
        ),
        migrations.AlterField(
            model_name='instancehistory',
            name='from_user',
            field=models.ForeignKey(related_name='from_history', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
