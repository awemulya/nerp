# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_imprestjournalvoucher_project_fy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imprestjournalvoucher',
            name='cr',
            field=models.ForeignKey(related_name='crediting_vouchers', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='imprestjournalvoucher',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='imprestjournalvoucher',
            name='dr',
            field=models.ForeignKey(related_name='debiting_vouchers', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='projectfy',
            name='imprest_ledger',
            field=models.ForeignKey(related_name='imprest_for', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='projectfy',
            name='initial_deposit',
            field=models.ForeignKey(related_name='deposit_for', to='account.Account'),
        ),
        migrations.AlterField(
            model_name='projectfy',
            name='replenishments',
            field=models.ForeignKey(related_name='replenishments_for', to='account.Account'),
        ),
    ]
