# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20151102_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instancehistory',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, verbose_name='Date', validators=[core.models.validate_in_fy]),
        ),
        migrations.AlterField(
            model_name='instancehistory',
            name='from_location',
            field=models.ForeignKey(related_name='from_history', verbose_name='From Location', to='inventory.ItemLocation'),
        ),
        migrations.AlterField(
            model_name='instancehistory',
            name='from_user',
            field=models.ForeignKey(related_name='from_history', verbose_name='From User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='instancehistory',
            name='to_location',
            field=models.ForeignKey(related_name='to_history', verbose_name='To Location', blank=True, to='inventory.ItemLocation', null=True),
        ),
        migrations.AlterField(
            model_name='instancehistory',
            name='to_user',
            field=models.ForeignKey(related_name='to_history', verbose_name='To User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
