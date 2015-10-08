# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fiscal_years(apps, schema_editor):
	from core.models import FiscalYear
	# FiscalYear = apps.get_model('core', 'FiscalYear')
	FiscalYear.objects.create(name=2069)

	FiscalYear.objects.create(year=2070)

	FiscalYear.objects.create(year=2071)


class Migration(migrations.Migration):

	dependencies = [
		('core', '0002_auto_20151007_2145'),
	]

	operations = [
		migrations.RunPython(fiscal_years),
	]


