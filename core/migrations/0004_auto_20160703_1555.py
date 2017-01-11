# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-03 10:10
from __future__ import unicode_literals

from django.db import migrations

def initialize_currencies(apps, schema_editor):
    from core.models import Currency

    Currency.objects.create(code="USD", name="United States, Dollar")
    Currency.objects.create(code="EUR", name="Euro")
    Currency.objects.create(code="NPR", name="Nepalese Rupee")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_budgethead_recurrent'),
    ]

    operations = [
        migrations.RunPython(initialize_currencies),
    ]
