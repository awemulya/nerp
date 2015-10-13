# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def item_location(apps, schema_editor):
    from inventory.models import ItemLocation

    ItemLocation.objects.create(name='Store')


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(item_location),
    ]
