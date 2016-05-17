# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0078_auto_20160516_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marital_status', models.CharField(default=b'U', max_length=1, choices=[(b'M', 'Married'), (b'U', 'Unmarried')])),
            ],
        ),
    ]
