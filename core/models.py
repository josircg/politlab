# -*- coding: utf-8 -*-
import os
import uuid
import requests

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings

from datetime import datetime
from decimal import Decimal

from core import choices


class Pessoa(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100, db_index=True)
    sexo = models.CharField(choices=choices.SEXO, max_length=1)

    def __str__(self):
        return u'%s' % self.nome


class Candidato(Pessoa):
    num_acessos = models.BigIntegerField(u'Número de Acessos', default=0)

    def get_absolute_url(self):
        return reverse('candidatos_detalhe', kwargs={'pk': self.pk})

    def nome_publico(self):
        try: return self.nomepublico_set.filter(num_acessos__gte=0)[0].nome
        except: return None

    def ultima_candidatura(self):
        try: return self.candidatura_set.order_by('-ano')[0]
        except: return None

    def __str__(self):
        return u'%s' % (self.nome)

    class Meta:
        ordering = ['cpf']


class NomePublico(models.Model):
    class Meta:
        verbose_name = u'Nome Público'
        verbose_name_plural = u'Nomes Públicos'
        unique_together = (('nome', 'pessoa'), )

    pessoa = models.ForeignKey(Pessoa)
    nome = models.CharField(max_length=100)
    num_acessos = models.BigIntegerField(u'Número de Acessos', default=0)

    def __str__(self):
        return u'%s' % (self.nome)


class Partido(models.Model):
    numero = models.PositiveSmallIntegerField(u'Número', db_index=True)
    sigla = models.CharField(max_length=20)
    nome = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s (%d)' % (self.sigla, self.numero)

    class Meta:
        ordering = ['sigla']


class Coligacao(models.Model):
    class Meta:
        verbose_name = 'Coligação'
        unique_together = (('ano', 'cargo', 'codigo',), )

    ano = models.PositiveSmallIntegerField()
    cargo = models.PositiveSmallIntegerField(choices=choices.CARGO_CHOICES)
    codigo = models.CharField(u'Código', max_length=20)
    nome = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return u'%s %s %s' % (self.ano, self.cargo, self.nome)


class UE(models.Model):
    class Meta:
        unique_together = (('sigla', 'agreg_regiao',), )
        verbose_name = 'Localidade'

    sigla = models.CharField(max_length=10)
    agreg_regiao = models.PositiveSmallIntegerField(choices=choices.LOCAL_CHOICES)
    descricao = models.CharField(max_length=100)
    UF = models.CharField(max_length=2)

    def __str__(self):
        if self.agreg_regiao == choices.AGR_REGIONAL.MUNICIPIO:
            return u'%s/%s' % (self.descricao, self.UF)
        else:
            return u'%s' % self.descricao


class Candidatura(models.Model):
    class Meta:
        index_together = (('ano', 'cargo', 'numero'), )
        ordering = ['-ano']

    candidato = models.ForeignKey(Candidato)
    ano = models.PositiveSmallIntegerField(db_index=True)
    cargo = models.PositiveSmallIntegerField(choices=choices.CARGO_CHOICES)
    agreg_regiao = models.PositiveSmallIntegerField(choices=choices.LOCAL_CHOICES)
    regiao = models.CharField(max_length=10)
    UE = models.ForeignKey(UE, blank=True, null=True)
    numero = models.IntegerField()
    partido = models.ForeignKey(Partido)
    coligacao = models.ForeignKey(Coligacao, null=True)
    num_votos = models.BigIntegerField(u'Núm.Votos', null=True)
    resultado = models.CharField(max_length=100)
    primeira = models.NullBooleanField(default=False)
    total_gasto = models.DecimalField(max_digits=12, decimal_places=2)
    eleito = models.NullBooleanField(null=True)

    def get_num_votos(self):
        if self.num_votos is None:
            try:
                url = 'http://cepesp.io/api/consulta/votos?columns[0][name]=NUMERO_CANDIDATO&columns[0][search][value]=%s' \
                    '&columns[1][name]=SIGLA_UE&columns[1][search][value]=%s&format=datatable&selected_columns[]=NUMERO_CANDIDATO' \
                    '&selected_columns[]=QTDE_VOTOS&selected_columns[]=SIGLA_UE&cargo=%s&anos[]=%s&agregacao_regional=%s' % (
                    self.numero, self.regiao, self.cargo, self.ano, self.UE.agreg_regiao
                )
                self.num_votos = requests.get(url).json().get('data', [])[0].get('QTDE_VOTOS')
                self.save()
            except: pass
        return self.num_votos

    def num_votos_partido(self):
        return Votacao.objects.filter(ano=self.ano, cargo=self.cargo, turno ='1', partido=self.partido).aggregate(num_votos=models.Sum('num_votos')).get('num_votos') or 0

    def num_candidatos_partido(self):
        return Candidatura.objects.filter(ano=self.ano, cargo=self.cargo, partido=self.partido, turno='1').count()

    def media_num_votos_partido(self):
        try:
            return round(float(self.num_votos_partido()) /float(self.num_candidatos_partido()), )
        except:
            return 0.0

    def num_votos_eleicao_para_cargo(self):
        return Votacao.objects.filter(ano=self.ano, cargo=self.cargo, turno='1').aggregate(num_votos=models.Sum('num_votos')).get('num_votos') or 0

    def percentual_num_votos_eleicao_para_cargo(self):
        try:
            return round(((float(self.num_votos)/float(self.num_votos_eleicao_para_cargo()))*100), 2)
        except:
            return 0.0

    def custo_do_voto(self):
        try:
            return round(self.total_gasto/self.get_num_votos(),2)
        except:
            return 0.0

    def get_absolute_url(self):
        return reverse('candidatura_detalhe', kwargs={'pk': self.pk})

    def __str__(self):
        return u'%s (%d)' % (self.candidato, self.ano)

class Votacao(models.Model):
    ano = models.PositiveSmallIntegerField()
    cargo = models.PositiveSmallIntegerField(choices=choices.CARGO_CHOICES)
    turno = models.CharField(max_length=1)
    partido = models.ForeignKey(Partido, null=True)
    UE = models.ForeignKey(UE, null=True)
    num_votos = models.BigIntegerField(u'Núm.Votos', default = 0)
    media = models.BigIntegerField(u'Média de Votos', null=True)

    class Meta:
        verbose_name = 'Votação por Partido'
        verbose_name_plural = 'Votações por Partido'
        unique_together = (('ano', 'cargo', 'UE', 'turno', 'partido', ), )
        ordering = ('ano',)

    def __str__(self):
        return u'%s (%s) %s (%s turno)' % (self.ano, self.cargo, self.partido, self.turno)


class SetorEconomico(models.Model):
    descricao = models.CharField(u'Descrição', max_length=255)

    class Meta:
        verbose_name = 'Setor Econômico'
        verbose_name_plural = 'Setores Econômicos'

    def __str__(self):
        return u'%s' % self.descricao


class Doador(models.Model):
    cpf = models.CharField(max_length=11, blank=True, null=True, db_index=True)
    cnpj = models.CharField(max_length=14, blank=True, null=True, db_index=True)
    partido = models.ForeignKey(Partido, blank=True, null=True)
    nome = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    setor = models.ForeignKey(SetorEconomico, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Doadores'

    def __str__(self):
        return u'%s' % self.nome


class Doacao(models.Model):
    candidatura = models.ForeignKey(Candidatura)
    doador = models.ForeignKey(Doador)
    dt = models.DateField(u'Dt. Doação')
    valor = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    valor_at = models.DecimalField(u'Valor atualizado', max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Doação'
        verbose_name_plural = 'Doações'

    def __str__(self):
        return '%s' % self.dt
