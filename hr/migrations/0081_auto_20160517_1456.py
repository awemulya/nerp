# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0080_auto_20160517_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxscheme',
            name='marital_status',
            field=models.ForeignKey(default=1, to='hr.MaritalStatus'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='taxscheme',
            unique_together=set([('marital_status', 'priority'), ('marital_status', 'start_from', 'end_to')]),
        ),
    ]
