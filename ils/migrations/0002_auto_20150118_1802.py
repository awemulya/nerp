# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ils', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(related_name=b'transactions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='ils.Subject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='authors',
            field=models.ManyToManyField(to='ils.Author', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='book',
            field=models.ForeignKey(to='ils.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='languages',
            field=models.ManyToManyField(to='core.Language', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='published_places',
            field=models.ManyToManyField(to='ils.Place', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='publisher',
            field=models.ForeignKey(blank=True, to='ils.Publisher', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookfile',
            name='record',
            field=models.ForeignKey(related_name=b'files', to='ils.Record'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='subjects',
            field=models.ManyToManyField(to='ils.Subject'),
            preserve_default=True,
        ),
    ]
