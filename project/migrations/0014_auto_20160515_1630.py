# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='project',
            field=models.ForeignKey(default=1, to='project.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expensecategory',
            name='project',
            field=models.ForeignKey(default=1, to='project.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expenserow',
            name='project',
            field=models.ForeignKey(default=1, to='project.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impresttransaction',
            name='project',
            field=models.ForeignKey(default=1, to='project.Project'),
            preserve_default=False,
        ),
    ]
