# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_budgethead_recurrent'),
        ('project', '0008_auto_20160630_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('rate', models.FloatField()),
                ('currency_from', models.ForeignKey(related_name='exchanged_from', to='core.Currency')),
                ('currency_to', models.ForeignKey(related_name='exchanged_to', to='core.Currency')),
            ],
        ),
    ]
