# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('hr', '0038_auto_20160420_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Journal Entries',
            },
        ),
        migrations.RenameField(
            model_name='account',
            old_name='acc_number',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='account',
            name='description',
        ),
        migrations.RemoveField(
            model_name='account',
            name='org_name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='debit',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='description',
        ),
        migrations.AddField(
            model_name='account',
            name='code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='current_cr',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='current_dr',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='opening_cr',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='opening_dr',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='cr_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='current_cr',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='current_dr',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='dr_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='journal_entry',
            field=models.ForeignKey(related_name='transactions', to='hr.JournalEntry', null=True),
        ),
    ]
