# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 12:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20171120_2302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='votacao',
            options={'verbose_name': 'Votação', 'verbose_name_plural': 'Votações'},
        ),
    ]
