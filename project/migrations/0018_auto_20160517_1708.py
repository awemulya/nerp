# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160516_1911'),
        ('project', '0017_project_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImprestLedger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fy', models.ForeignKey(to='core.FiscalYear')),
                ('ledger', models.ForeignKey(to='core.Account')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='imprestledger',
            unique_together=set([('project', 'fy')]),
        ),
    ]
