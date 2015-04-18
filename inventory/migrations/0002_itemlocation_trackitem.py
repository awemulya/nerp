# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrackItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('other_properties', models.CharField(max_length=200, null=True, blank=True)),
                ('item', models.ForeignKey(related_name=b'tracked_item', to='inventory.Item')),
                ('location', models.ForeignKey(to='inventory.ItemLocation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
