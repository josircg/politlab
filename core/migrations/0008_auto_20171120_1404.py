# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171120_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatura',
            name='resultado',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]