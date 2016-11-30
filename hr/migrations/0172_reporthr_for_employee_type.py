# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-30 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0171_employee_pf_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporthr',
            name='for_employee_type',
            field=models.CharField(choices=[(b'PERMANENT', 'Permanent'), (b'TEMPORARY', 'Temporary')], default='PERMANENT', max_length=50),
            preserve_default=False,
        ),
    ]
