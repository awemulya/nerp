# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0082_auto_20160517_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxcalcscheme',
            name='scheme',
            field=models.ForeignKey(related_name='tax_calc_scheme', to='hr.TaxScheme'),
        ),
        migrations.AlterField(
            model_name='taxscheme',
            name='marital_status',
            field=models.ForeignKey(related_name='tax_scheme', to='hr.MaritalStatus'),
        ),
    ]
