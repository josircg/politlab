# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 14:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_candidatura_partido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coligacao',
            name='agreg_regiao',
        ),
        migrations.RemoveField(
            model_name='coligacao',
            name='regiao',
        ),
    ]
