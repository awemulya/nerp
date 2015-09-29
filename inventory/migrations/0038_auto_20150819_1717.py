# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_quotationcomparison_release_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationcomparisonrow',
            name='party',
        ),
        migrations.AddField(
            model_name='partyquotation',
            name='quotation_comparison_row',
            field=models.ForeignKey(related_name='bidder_quote', blank=True, to='inventory.QuotationComparisonRow', null=True),
        ),
    ]
