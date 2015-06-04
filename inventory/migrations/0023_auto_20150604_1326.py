# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_trackitem_item_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_rate', models.FloatField(null=True)),
                ('other_properties', jsonfield.fields.JSONField(null=True, blank=True)),
                ('item', models.ForeignKey(related_name='tracked_item', to='inventory.Item')),
                ('location', models.ForeignKey(to='inventory.ItemLocation')),
            ],
        ),
        migrations.RemoveField(
            model_name='trackitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='trackitem',
            name='location',
        ),
        migrations.DeleteModel(
            name='TrackItem',
        ),
    ]
