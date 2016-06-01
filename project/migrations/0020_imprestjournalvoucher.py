# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160518_1618'),
        ('project', '0019_auto_20160517_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImprestJournalVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('amount_nrs', models.FloatField(null=True, blank=True)),
                ('amount_usd', models.FloatField(null=True, blank=True)),
                ('exchange_rate', models.FloatField(null=True, blank=True)),
                ('wa_no', models.CharField(max_length=10, null=True, blank=True)),
                ('cr', models.ForeignKey(related_name='crediting_vouchers', to='core.Account')),
                ('dr', models.ForeignKey(related_name='debiting_vouchers', to='core.Account')),
            ],
        ),
    ]
