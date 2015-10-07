# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fiscal_years(apps, schema_editor):
	import ipdb; ipdb.set_trace()
	print "test"
	from core.models import FiscalYear

	FiscalYear.objects.create(year=2070)
	FiscalYear.objects.create(year=2071)



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(fiscal_years),
    ]
