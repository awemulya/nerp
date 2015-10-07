# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.db import transaction


def initialize(apps, schema_editor):
	from users.models import User
	from django.contrib.auth.models import Group
	import ipdb; ipdb.set_trace()

	Group.objects.create(name='Store')

	try:
		with transaction.atomic():
			admin = User.objects.create_superuser('admin', 'webadmin@awecode.com', 'admin')
	except IntegrityError:
		admin = User.objects.get(username='admin')


class Migration(migrations.Migration):
	dependencies = [
		('users', '0001_initial'),
	]

	operations = [
		migrations.RunPython(initialize),
	]
