# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_candidatura_ue'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidato',
            options={'ordering': ['cpf']},
        ),
        migrations.AlterModelOptions(
            name='candidatura',
            options={'ordering': ['-ano']},
        ),
        migrations.AlterModelOptions(
            name='partido',
            options={'ordering': ['sigla']},
        ),
        migrations.AddField(
            model_name='candidatura',
            name='eleito',
            field=models.NullBooleanField(),
        ),
    ]