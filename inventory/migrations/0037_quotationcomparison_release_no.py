# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0036_partyquotation_quotationcomparison_quotationcomparisonrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationcomparison',
            name='release_no',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
