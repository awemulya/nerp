# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, IntegrityError
from django.db import transaction


def initialize(apps, schema_editor):
	from users.models import User
	from django.contrib.auth.models import Group

	Group.objects.create(name='Chief')
	Group.objects.create(name='Store Keeper')
	Group.objects.create(name='Accountant')
	Group.objects.create(name='Staff')
	Group.objects.create(name='Patron')
	Group.objects.create(name='Librarian')
	Group.objects.create(name='Trainer')

	try:
		with transaction.atomic():
			admin = User.objects.create_superuser('admin', 'webadmin@awecode.com', 'admin')
	except IntegrityError:
		admin = User.objects.get(username='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151007_2107'),
    ]

    operations = [
    	migrations.RunPython(initialize),
    ]
