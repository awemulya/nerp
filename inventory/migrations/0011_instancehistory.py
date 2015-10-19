# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import core.models
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0010_iteminstance_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, validators=[core.models.validate_in_fy])),
                ('from_location', models.ForeignKey(related_name='from_history', to='inventory.ItemLocation')),
                ('from_user', models.ForeignKey(related_name='from_history', to=settings.AUTH_USER_MODEL)),
                ('instance', models.ForeignKey(to='inventory.ItemInstance')),
                ('to_location', models.ForeignKey(related_name='to_history', to='inventory.ItemLocation')),
                ('to_user', models.ForeignKey(related_name='to_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
