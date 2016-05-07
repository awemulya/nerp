# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0056_auto_20160507_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deduction',
            old_name='taxable',
            new_name='is_tax_free',
        ),
    ]
