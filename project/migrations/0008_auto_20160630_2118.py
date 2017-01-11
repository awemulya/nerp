# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from app.utils.helpers import truncate_model


def delete_aids(apps, schema):
    from project.models import Aid

    try:
        truncate_model(Aid)
    except Exception as e:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0003_auto_20160630_1205'),
        ('project', '0007_auto_20160630_1346'),
    ]

    operations = [
        migrations.RunPython(delete_aids),
        migrations.RemoveField(
            model_name='projectfy',
            name='imprest_ledger',
        ),
        migrations.AddField(
            model_name='aid',
            name='imprest_ledger',
            field=models.ForeignKey(related_name='imprest_for', default=None, to='account.Account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aid',
            name='project',
            field=models.ForeignKey(related_name='aids', to='project.Project'),
        ),
        migrations.AlterField(
            model_name='disbursementdetail',
            name='aid',
            field=models.ForeignKey(related_name='disbursements', to='project.Aid'),
        ),
    ]
