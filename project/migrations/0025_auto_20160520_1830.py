# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetallocationitem',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='budgetallocationitem',
            name='project',
        ),
        migrations.RemoveField(
            model_name='budgetreleaseitem',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='budgetreleaseitem',
            name='project',
        ),
        migrations.RemoveField(
            model_name='expenditure',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='expenditure',
            name='project',
        ),
        migrations.AddField(
            model_name='budgetallocationitem',
            name='project_fy',
            field=models.ForeignKey(default=1, to='project.ProjectFy'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='budgetreleaseitem',
            name='project_fy',
            field=models.ForeignKey(default=1, to='project.ProjectFy'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expenditure',
            name='project_fy',
            field=models.ForeignKey(default=1, to='project.ProjectFy'),
            preserve_default=False,
        ),
    ]
