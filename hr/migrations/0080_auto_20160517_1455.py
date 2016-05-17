# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0079_maritalstatus'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taxscheme',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='taxscheme',
            name='marital_status',
        ),
    ]
