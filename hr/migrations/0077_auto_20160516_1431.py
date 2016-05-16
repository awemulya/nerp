# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0076_auto_20160515_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxCalcScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_from', models.FloatField()),
                ('end_to', models.FloatField(null=True, blank=True)),
                ('tax_rate', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='taxscheme',
            unique_together=set([('marital_status', 'start_from', 'end_to')]),
        ),
        migrations.AddField(
            model_name='taxcalcscheme',
            name='scheme',
            field=models.ForeignKey(to='hr.TaxScheme'),
        ),
        migrations.RemoveField(
            model_name='taxscheme',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='taxscheme',
            name='tax_rate',
        ),
    ]
