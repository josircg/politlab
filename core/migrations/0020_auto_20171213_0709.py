# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20171212_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doacao',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]