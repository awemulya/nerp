# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20160515_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signatory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('default', models.BooleanField(default=False, verbose_name=b'Required to sign on all notes?')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
        ),
    ]
