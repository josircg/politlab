# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20171211_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatura',
            name='total_gasto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
    ]