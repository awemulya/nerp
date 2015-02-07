# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.flexible_date


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0004_auto_20150201_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCustomDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', app.utils.flexible_date.FlexibleDateField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='record',
            name='publication_has_day',
        ),
        migrations.RemoveField(
            model_name='record',
            name='publication_has_month',
        ),
        migrations.AlterField(
            model_name='record',
            name='book',
            field=models.ForeignKey(to='ils.Book', blank=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='date_of_publication',
            field=app.utils.flexible_date.FlexibleDateField(null=True, blank=True),
        ),
    ]
