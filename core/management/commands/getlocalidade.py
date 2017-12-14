# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from core.models import UE
from core.choices import *

import pandas as pd
import requests
import hashlib
import os
from random import randint

class Command(BaseCommand):
    help = 'Monta base de Localidade'

    def handle(self, *args, **options):

        def save_cache(content, filepath):
            with open(filepath, 'wb') as outfile:
                outfile.write(content)

        print('Iniciando importação')
        for agreg_regiao, ano, cargo in ((AGR_REGIONAL.UF, 2014, 3), (AGR_REGIONAL.MUNICIPIO, 2016, 11)):

            url = 'http://cepesp.io/api/consulta/votos?cargo=%s&ano=%s&agregacao_regional=%s&agregacao_politica=4&format=gzip' % (cargo, ano, agreg_regiao)
            filename = u'%s.gz' % hashlib.md5(url.encode('utf-8')).hexdigest()

            # Cria diretório de cache
            if not os.path.exists(os.path.join(settings.BASE_DIR, "cache")):
                os.makedirs(os.path.join(settings.BASE_DIR, "cache"))

            filepath = os.path.join(settings.BASE_DIR, "cache/" + filename)
            content = requests.get(url).content
            save_cache(content, filepath)

            if agreg_regiao == AGR_REGIONAL.UF:
                descricao = 'NOME_UF'
            elif agreg_regiao == AGR_REGIONAL.MUNICIPIO:
                descricao = 'NOME_MUNICIPIO'

            count = 0
            dataframe = pd.read_csv(filepath, sep=",", dtype=str)
            for index, data in dataframe.sort_values('NUM_TURNO').iterrows():

                ue, created = UE.objects.get_or_create(
                    sigla=data['SIGLA_UE'],
                    agreg_regiao=agreg_regiao,
                    descricao=data[descricao],
                    UF=data['UF'],
                )
                if created:
                    count += 1
            print('Agregação %s: %d importados' % (agreg_regiao, count))