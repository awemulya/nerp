# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0077_auto_20160516_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxcalcscheme',
            name='priority',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxscheme',
            name='priority',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='taxcalcscheme',
            unique_together=set([('scheme', 'priority'), ('scheme', 'start_from', 'end_to')]),
        ),
        migrations.AlterUniqueTogether(
            name='taxscheme',
            unique_together=set([('marital_status', 'priority'), ('marital_status', 'start_from', 'end_to')]),
        ),
    ]
