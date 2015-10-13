# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def item_location(apps, schema_editor):
	from inventory.models import ItemLocation

	ItemLocation.objects.create(name='Store')


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151007_2104'),
    ]

    operations = [
    	migrations.RunPython(item_location),
    ]
