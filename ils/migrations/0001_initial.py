# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('identifier', models.CharField(max_length=50, null=True, blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('subtitle', models.CharField(max_length=254, null=True, blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'ils/books/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edition', models.CharField(max_length=254, null=True, blank=True)),
                ('format', models.CharField(default=b'Paperback', max_length=10, choices=[(b'Paperback', b'Paperback'), (b'Hardcover', b'Hardcover'), (b'eBook', b'eBook')])),
                ('pagination', models.CharField(max_length=254, null=True, blank=True)),
                ('isbn13', models.CharField(max_length=254, null=True, blank=True)),
                ('date_of_publication', models.DateField(null=True, blank=True)),
                ('publication_has_month', models.BooleanField(default=True)),
                ('publication_has_day', models.BooleanField(default=True)),
                ('price', models.FloatField(null=True, blank=True)),
                ('quantity', models.PositiveIntegerField(default=1, null=True, blank=True)),
                ('type', models.CharField(max_length=11, choices=[(b'Reference', b'Reference'), (b'Circulative', b'Circulative')])),
                ('small_cover', models.ImageField(null=True, upload_to=b'ils/covers/small/', blank=True)),
                ('medium_cover', models.ImageField(null=True, upload_to=b'ils/covers/medium/', blank=True)),
                ('large_cover', models.ImageField(null=True, upload_to=b'ils/covers/large/', blank=True)),
                ('date_added', models.DateField()),
                ('goodreads_id', models.PositiveIntegerField(null=True, blank=True)),
                ('librarything_id', models.PositiveIntegerField(null=True, blank=True)),
                ('openlibrary_id', models.CharField(max_length=254, null=True, blank=True)),
                ('lcc', models.CharField(max_length=100, null=True, blank=True)),
                ('ddc', models.CharField(max_length=100, null=True, blank=True)),
                ('lccn_id', models.CharField(max_length=100, null=True, blank=True)),
                ('oclc_id', models.CharField(max_length=100, null=True, blank=True)),
                ('weight', models.CharField(max_length=254, null=True, blank=True)),
                ('dimensions', models.CharField(max_length=254, null=True, blank=True)),
                ('by_statement', models.CharField(max_length=254, null=True, blank=True)),
                ('notes', models.CharField(max_length=254, null=True, blank=True)),
                ('excerpt', models.CharField(max_length=254, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('borrow_date', models.DateField()),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(null=True, blank=True)),
                ('returned', models.BooleanField(default=False)),
                ('fine_per_day', models.FloatField()),
                ('fine_paid', models.FloatField(default=False)),
                ('record', models.ForeignKey(to='ils.Record')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
