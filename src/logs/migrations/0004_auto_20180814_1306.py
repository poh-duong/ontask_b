# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-14 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_auto_20180530_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='payload',
            field=models.TextField(default=''),
        ),
    ]