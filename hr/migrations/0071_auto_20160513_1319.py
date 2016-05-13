# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0070_remove_incometaxrate_rate_over_tax_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IncomeTaxRate',
            new_name='TaxScheme',
        ),
    ]
