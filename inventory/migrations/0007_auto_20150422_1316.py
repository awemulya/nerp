# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_yearlyreport_yearlyrow'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='YearlyRow',
            new_name='YearlyReportRow',
        ),
    ]
