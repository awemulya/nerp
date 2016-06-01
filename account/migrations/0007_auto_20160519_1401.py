# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160518_1618'),
        ('account', '0006_auto_20160517_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='account',
            name='fy',
            field=models.ForeignKey(blank=True, to='core.FiscalYear', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='journalvoucherrow',
            name='account',
            field=models.ForeignKey(to='account.Account'),
        ),
        migrations.AlterField(
            model_name='receiptrow',
            name='account',
            field=models.ForeignKey(to='account.Account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(to='account.Account'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('name', 'fy')]),
        ),
    ]
