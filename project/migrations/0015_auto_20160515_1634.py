# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_currency'),
        ('project', '0014_auto_20160515_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10, choices=[(b'loan', b'Loan'), (b'grant', b'Grant')])),
                ('key', models.CharField(max_length=50)),
                ('donor', models.ForeignKey(to='core.Donor')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='key',
        ),
        migrations.AddField(
            model_name='aid',
            name='project',
            field=models.ForeignKey(to='project.Project'),
        ),
    ]
