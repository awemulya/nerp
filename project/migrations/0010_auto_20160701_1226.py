# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_budgethead_recurrent'),
        ('project', '0009_exchangerate'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPRExchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('rate', models.FloatField()),
                ('currency', models.ForeignKey(related_name='npr_exchanges', to='core.Currency')),
            ],
        ),
        migrations.RemoveField(
            model_name='exchangerate',
            name='currency_from',
        ),
        migrations.RemoveField(
            model_name='exchangerate',
            name='currency_to',
        ),
        migrations.DeleteModel(
            name='ExchangeRate',
        ),
    ]
