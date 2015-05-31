# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resourceperson',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='categories',
            field=models.ManyToManyField(related_name='trainings', to='training.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='participants',
            field=models.ManyToManyField(related_name='trainings', to='training.Participant', blank=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='resource_persons',
            field=models.ManyToManyField(related_name='trainings', to='training.ResourcePerson', blank=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='target_groups',
            field=models.ManyToManyField(related_name='trainings', to='training.TargetGroup', blank=True),
        ),
    ]
