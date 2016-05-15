# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0075_auto_20160515_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxscheme',
            name='priority',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='taxscheme',
            unique_together=set([('marital_status', 'start_from', 'end_to'), ('priority', 'marital_status')]),
        ),
    ]
