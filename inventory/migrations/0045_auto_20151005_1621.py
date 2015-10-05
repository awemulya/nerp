# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0044_auto_20151005_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotationcomparison',
            old_name='release_no',
            new_name='report_no',
        ),
    ]
