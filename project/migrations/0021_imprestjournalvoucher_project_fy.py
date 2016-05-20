# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_imprestjournalvoucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='imprestjournalvoucher',
            name='project_fy',
            field=models.ForeignKey(default=1, to='project.ProjectFy'),
            preserve_default=False,
        ),
    ]
