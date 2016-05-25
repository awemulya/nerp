# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160516_1911'),
        ('project', '0018_auto_20160517_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectFy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fy', models.ForeignKey(to='core.FiscalYear')),
                ('imprest_ledger', models.ForeignKey(related_name='imprest_for', to='core.Account')),
                ('initial_deposit', models.ForeignKey(related_name='deposit_for', to='core.Account')),
                ('project', models.ForeignKey(to='project.Project')),
                ('replenishments', models.ForeignKey(related_name='replenishments_for', to='core.Account')),
            ],
            options={
                'verbose_name': 'Project Fiscal Year',
                'verbose_name_plural': 'Project Fiscal Years',
            },
        ),
        migrations.AlterUniqueTogether(
            name='imprestledger',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='imprestledger',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='imprestledger',
            name='ledger',
        ),
        migrations.RemoveField(
            model_name='imprestledger',
            name='project',
        ),
        migrations.AlterModelOptions(
            name='signatory',
            options={'verbose_name_plural': 'Signatories'},
        ),
        migrations.RemoveField(
            model_name='expenserow',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='expenserow',
            name='project',
        ),
        migrations.RemoveField(
            model_name='impresttransaction',
            name='fy',
        ),
        migrations.RemoveField(
            model_name='impresttransaction',
            name='project',
        ),
        migrations.DeleteModel(
            name='ImprestLedger',
        ),
        migrations.AddField(
            model_name='expenserow',
            name='project_fy',
            field=models.ForeignKey(default=1, to='project.ProjectFy'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='impresttransaction',
            name='project_fy',
            field=models.ForeignKey(default=1, to='project.ProjectFy'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='projectfy',
            unique_together=set([('project', 'fy')]),
        ),
    ]
