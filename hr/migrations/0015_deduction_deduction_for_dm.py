# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


def set_deduction_for(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Deduction = apps.get_model("hr", "Deduction")
    for d in Deduction.objects.all():
        d.deduction_for = 'EMPLOYEE ACC'
        d.save()
        # person.name = "%s %s" % (person.first_name, person.last_name)
        # person.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('hr', '0014_auto_20160330_1325'),
    ]

    operations = [
        migrations.RunPython(set_deduction_for),
    ]
