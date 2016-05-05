# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0048_auto_20160506_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allowance',
            old_name='a_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='incentive',
            old_name='i_name',
            new_name='name',
        ),
        migrations.AlterUniqueTogether(
            name='allowance',
            unique_together=set([('name', 'employee_grade')]),
        ),
        migrations.AlterUniqueTogether(
            name='incentive',
            unique_together=set([('name', 'employee_grade')]),
        ),
    ]
