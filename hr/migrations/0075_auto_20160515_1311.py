# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0074_auto_20160515_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxscheme',
            name='marital_status',
            field=models.CharField(default=b'U', max_length=1, choices=[(b'M', 'Married'), (b'U', 'Unmarried')]),
        ),
        migrations.AlterUniqueTogether(
            name='taxscheme',
            unique_together=set([('marital_status', 'start_from', 'end_to')]),
        ),
    ]
