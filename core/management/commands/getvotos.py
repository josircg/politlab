# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from core.models import Candidato, Partido, Votacao
from core.choices import *

import pandas as pd
import requests
import hashlib
import os


def gen_id(s):
    h = hashlib.sha256(s)
    return h.digest().encode('base64')[:6]

class Command(BaseCommand):
    help = 'Monta totalizador de votos por partido'

    def handle(self, *args, **options):

        def save_cache(content, filepath):
            with open(filepath, 'wb') as outfile:
                outfile.write(content)

        for ano, cargos in ANO_CARGOS.items():

            for cargo in cargos:
                url = 'http://cepesp.io/api/consulta/tse?cargo=%s&ano=%s&agregacao_regional=0&agregacao_politica=2' % (cargo, ano)
                filename = u'%s' % hashlib.md5(url.encode('utf-8')).hexdigest()

                print('Cargo %s: Ano %d' % (cargo, ano))
                # Cria diretório de cache
                if not os.path.exists(os.path.join(settings.BASE_DIR, "cache")):
                    os.makedirs(os.path.join(settings.BASE_DIR, "cache"))

                filepath = os.path.join(settings.BASE_DIR, "cache/" + filename)
                content = requests.get(url).content
                save_cache(content, filepath)

                if Votacao.objects.filter(ano=ano, cargo=cargo).exists():
                    print('excluindo candidaturas existentes')
                    Votacao.objects.filter(ano=ano, cargo=cargo).delete()

                # Insere registros agregados dos partidos
                count = 0
                inclusao = 0
                count_candidatos = 0
                dataframe = pd.read_csv(filepath, sep=",", dtype=str)
                for index, data in dataframe.iterrows():
                    count += 1

                    try:
                        numero_partido = int(data['NUMERO_PARTIDO'])
                    except:
                        print('Linha %d: Número de Partido inválido:[%s]' % (count, data['NUMERO_PARTIDO']))
                        continue

                    if numero_partido in (97,98):
                        continue

                    try:
                        partido = Partido.objects.get(sigla=data['SIGLA_PARTIDO'], numero=numero_partido)
                    except Partido.DoesNotExist:
                        print('Partido não encontrado:[%s]' % data['SIGLA_PARTIDO'])
                        continue

                    votacao, created = Votacao.objects.get_or_create(
                        ano = ano,
                        cargo = cargo,
                        turno = data['NUM_TURNO'],
                        partido = partido)
                    votacao.num_votos += int(float(data['QTDE_VOTOS']))
                    votacao.save()

                    if created:
                        inclusao += 1

                print('Registros lidos: %d ' % count)
                print('Adicionados: %d' % inclusao)