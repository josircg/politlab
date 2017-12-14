# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20171209_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateField(verbose_name='Dt. Doação')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('valor_at', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Valor atualizado')),
                ('candidatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Candidatura')),
            ],
            options={
                'verbose_name': 'Doação',
                'verbose_name_plural': 'Doações',
            },
        ),
        migrations.CreateModel(
            name='Doador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=11, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True)),
                ('nome', models.CharField(max_length=200)),
                ('uf', models.CharField(max_length=2)),
                ('partido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Partido')),
            ],
            options={
                'verbose_name_plural': 'Doadores',
            },
        ),
        migrations.CreateModel(
            name='SetorEconomico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='doador',
            name='setor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.SetorEconomico'),
        ),
        migrations.AddField(
            model_name='doacao',
            name='doador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Doador'),
        ),
    ]
