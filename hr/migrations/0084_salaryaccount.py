# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0083_auto_20160519_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(related_name='salary_account', to='hr.Account')),
            ],
        ),
    ]
