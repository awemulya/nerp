# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=254, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='training.Category', null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=b'training/files/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(null=True, blank=True)),
                ('phone_no', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('fax', models.CharField(max_length=50, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(null=True, blank=True)),
                ('phone_no', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('organization', models.ForeignKey(blank=True, to='training.Organization', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourcePerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(null=True, blank=True)),
                ('phone_no', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('organization', models.ForeignKey(blank=True, to='training.Organization', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='training.TargetGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('description', models.TextField(null=True, blank=True)),
                ('starts', models.DateField(null=True, blank=True)),
                ('ends', models.DateField(null=True, blank=True)),
                ('criteria_for_selection', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('objective', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('output', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('conclusion', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('feedback', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('curriculum', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('categories', models.ManyToManyField(related_name='trainings', to='training.Category', blank=True)),
                ('participants', models.ManyToManyField(related_name='trainings', to='training.Participant', blank=True)),
                ('resource_persons', models.ManyToManyField(related_name='trainings', to='training.ResourcePerson', blank=True)),
                ('target_groups', models.ManyToManyField(related_name='trainings', to='training.TargetGroup', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='training',
            field=models.ForeignKey(related_name='files', to='training.Training'),
        ),
    ]
