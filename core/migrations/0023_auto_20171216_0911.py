# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 12:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20171216_0855'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nomepublico',
            unique_together=set([('nome', 'pessoa')]),
        ),
    ]
