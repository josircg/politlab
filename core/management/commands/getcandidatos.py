# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from core.models import Candidato, Candidatura, NomePublico, Partido, Coligacao, UE
from core.choices import *

import pandas as pd
import requests
import hashlib
import os
import sys
from random import randint

class Command(BaseCommand):
    help = 'Monta base de candidatos'

    def handle(self, *args, **options):
        def clean_cpf(cpf):
            if len(cpf) < 11:
                return ('0'*(11-len(cpf)))+cpf
            return cpf

        def gen_id(s):
            return abs(hash(s)) % (10 ** 9)

        def save_cache(content, filepath):
            with open(filepath, 'wb') as outfile:
                outfile.write(content)

        cpf_ident = 0
        for ano, cargos in ANO_CARGOS.items():

            for cargo in cargos:

                print('Iniciando importação %d %d' % (ano, cargo))

                url = 'http://cepesp.io/api/consulta/candidatos?draw=1&columns[0][data]=DATA_GERACAO' \
                    '&columns[0][name]=DATA_GERACAO&columns[0][searchable]=true&columns[0][orderable]=false' \
                    '&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=HORA_GERACAO' \
                    '&columns[1][name]=HORA_GERACAO&columns[1][searchable]=true&columns[1][orderable]=false' \
                    '&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=ANO_ELEICAO' \
                    '&columns[2][name]=ANO_ELEICAO&columns[2][searchable]=true&columns[2][orderable]=false' \
                    '&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=NUM_TURNO' \
                    '&columns[3][name]=NUM_TURNO&columns[3][searchable]=true&columns[3][orderable]=false' \
                    '&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=DESCRICAO_ELEICAO' \
                    '&columns[4][name]=DESCRICAO_ELEICAO&columns[4][searchable]=true&columns[4][orderable]=false' \
                    '&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=SIGLA_UF' \
                    '&columns[5][name]=SIGLA_UF&columns[5][searchable]=true&columns[5][orderable]=false' \
                    '&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=SIGLA_UE' \
                    '&columns[6][name]=SIGLA_UE&columns[6][searchable]=true&columns[6][orderable]=false' \
                    '&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=DESCRICAO_UE' \
                    '&columns[7][name]=DESCRICAO_UE&columns[7][searchable]=true&columns[7][orderable]=false' \
                    '&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=CODIGO_CARGO' \
                    '&columns[8][name]=CODIGO_CARGO&columns[8][searchable]=true&columns[8][orderable]=false' \
                    '&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=DESCRICAO_CARGO' \
                    '&columns[9][name]=DESCRICAO_CARGO&columns[9][searchable]=true&columns[9][orderable]=false' \
                    '&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=NUMERO_PARTIDO' \
                    '&columns[10][name]=NUMERO_PARTIDO&columns[10][searchable]=true&columns[10][orderable]=false' \
                    '&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=SIGLA_PARTIDO' \
                    '&columns[11][name]=SIGLA_PARTIDO&columns[11][searchable]=true&columns[11][orderable]=false' \
                    '&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=NOME_CANDIDATO' \
                    '&columns[12][name]=NOME_CANDIDATO&columns[12][searchable]=true&columns[12][orderable]=false' \
                    '&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=NUMERO_CANDIDATO' \
                    '&columns[13][name]=NUMERO_CANDIDATO&columns[13][searchable]=true&columns[13][orderable]=false' \
                    '&columns[13][search][value]=&columns[13][search][regex]=false&columns[14][data]=CPF_CANDIDATO' \
                    '&columns[14][name]=CPF_CANDIDATO&columns[14][searchable]=true&columns[14][orderable]=false' \
                    '&columns[14][search][value]=&columns[14][search][regex]=false&columns[15][data]=NOME_URNA_CANDIDATO' \
                    '&columns[15][name]=NOME_URNA_CANDIDATO&columns[15][searchable]=true&columns[15][orderable]=false' \
                    '&columns[15][search][value]=&columns[15][search][regex]=false&columns[16][data]=COD_SITUACAO_CANDIDATURA' \
                    '&columns[16][name]=COD_SITUACAO_CANDIDATURA&columns[16][searchable]=true&columns[16][orderable]=false' \
                    '&columns[16][search][value]=&columns[16][search][regex]=false&columns[17][data]=DES_SITUACAO_CANDIDATURA' \
                    '&columns[17][name]=DES_SITUACAO_CANDIDATURA&columns[17][searchable]=true&columns[17][orderable]=false' \
                    '&columns[17][search][value]=&columns[17][search][regex]=false&columns[18][data]=NOME_PARTIDO' \
                    '&columns[18][name]=NOME_PARTIDO&columns[18][searchable]=true&columns[18][orderable]=false' \
                    '&columns[18][search][value]=&columns[18][search][regex]=false&columns[19][data]=CODIGO_LEGENDA' \
                    '&columns[19][name]=CODIGO_LEGENDA&columns[19][searchable]=true&columns[19][orderable]=false' \
                    '&columns[19][search][value]=&columns[19][search][regex]=false&columns[20][data]=SIGLA_LEGENDA' \
                    '&columns[20][name]=SIGLA_LEGENDA&columns[20][searchable]=true&columns[20][orderable]=false' \
                    '&columns[20][search][value]=&columns[20][search][regex]=false&columns[21][data]=COMPOSICAO_LEGENDA' \
                    '&columns[21][name]=COMPOSICAO_LEGENDA&columns[21][searchable]=true&columns[21][orderable]=false' \
                    '&columns[21][search][value]=&columns[21][search][regex]=false&columns[22][data]=NOME_COLIGACAO' \
                    '&columns[22][name]=NOME_COLIGACAO&columns[22][searchable]=true&columns[22][orderable]=false' \
                    '&columns[22][search][value]=&columns[22][search][regex]=false&columns[23][data]=CODIGO_OCUPACAO' \
                    '&columns[23][name]=CODIGO_OCUPACAO&columns[23][searchable]=true&columns[23][orderable]=false' \
                    '&columns[23][search][value]=&columns[23][search][regex]=false&columns[24][data]=DESCRICAO_OCUPACAO' \
                    '&columns[24][name]=DESCRICAO_OCUPACAO&columns[24][searchable]=true&columns[24][orderable]=false' \
                    '&columns[24][search][value]=&columns[24][search][regex]=false&columns[25][data]=DATA_NASCIMENTO' \
                    '&columns[25][name]=DATA_NASCIMENTO&columns[25][searchable]=true&columns[25][orderable]=false' \
                    '&columns[25][search][value]=&columns[25][search][regex]=false&columns[26][data]=NUM_TITULO_ELEITORAL_CANDIDATO' \
                    '&columns[26][name]=NUM_TITULO_ELEITORAL_CANDIDATO&columns[26][searchable]=true&columns[26][orderable]=false' \
                    '&columns[26][search][value]=&columns[26][search][regex]=false&columns[27][data]=IDADE_DATA_ELEICAO' \
                    '&columns[27][name]=IDADE_DATA_ELEICAO&columns[27][searchable]=true&columns[27][orderable]=false' \
                    '&columns[27][search][value]=&columns[27][search][regex]=false&columns[28][data]=CODIGO_SEXO' \
                    '&columns[28][name]=CODIGO_SEXO&columns[28][searchable]=true&columns[28][orderable]=false' \
                    '&columns[28][search][value]=&columns[28][search][regex]=false&columns[29][data]=DESCRICAO_SEXO' \
                    '&columns[29][name]=DESCRICAO_SEXO&columns[29][searchable]=true&columns[29][orderable]=false' \
                    '&columns[29][search][value]=&columns[29][search][regex]=false&columns[30][data]=COD_GRAU_INSTRUCAO' \
                    '&columns[30][name]=COD_GRAU_INSTRUCAO&columns[30][searchable]=true&columns[30][orderable]=false' \
                    '&columns[30][search][value]=&columns[30][search][regex]=false&columns[31][data]=DESCRICAO_GRAU_INSTRUCAO' \
                    '&columns[31][name]=DESCRICAO_GRAU_INSTRUCAO&columns[31][searchable]=true&columns[31][orderable]=false' \
                    '&columns[31][search][value]=&columns[31][search][regex]=false&columns[32][data]=CODIGO_ESTADO_CIVIL' \
                    '&columns[32][name]=CODIGO_ESTADO_CIVIL&columns[32][searchable]=true&columns[32][orderable]=false' \
                    '&columns[32][search][value]=&columns[32][search][regex]=false&columns[33][data]=DESCRICAO_ESTADO_CIVIL' \
                    '&columns[33][name]=DESCRICAO_ESTADO_CIVIL&columns[33][searchable]=true&columns[33][orderable]=false' \
                    '&columns[33][search][value]=&columns[33][search][regex]=false&columns[34][data]=CODIGO_NACIONALIDADE' \
                    '&columns[34][name]=CODIGO_NACIONALIDADE&columns[34][searchable]=true&columns[34][orderable]=false' \
                    '&columns[34][search][value]=&columns[34][search][regex]=false&columns[35][data]=DESCRICAO_NACIONALIDADE' \
                    '&columns[35][name]=DESCRICAO_NACIONALIDADE&columns[35][searchable]=true&columns[35][orderable]=false' \
                    '&columns[35][search][value]=&columns[35][search][regex]=false&columns[36][data]=SIGLA_UF_NASCIMENTO' \
                    '&columns[36][name]=SIGLA_UF_NASCIMENTO&columns[36][searchable]=true&columns[36][orderable]=false' \
                    '&columns[36][search][value]=&columns[36][search][regex]=false&columns[37][data]=CODIGO_MUNICIPIO_NASCIMENTO' \
                    '&columns[37][name]=CODIGO_MUNICIPIO_NASCIMENTO&columns[37][searchable]=true&columns[37][orderable]=false' \
                    '&columns[37][search][value]=&columns[37][search][regex]=false&columns[38][data]=NOME_MUNICIPIO_NASCIMENTO' \
                    '&columns[38][name]=NOME_MUNICIPIO_NASCIMENTO&columns[38][searchable]=true&columns[38][orderable]=false' \
                    '&columns[38][search][value]=&columns[38][search][regex]=false&columns[39][data]=DESPESA_MAX_CAMPANHA' \
                    '&columns[39][name]=DESPESA_MAX_CAMPANHA&columns[39][searchable]=true&columns[39][orderable]=false' \
                    '&columns[39][search][value]=&columns[39][search][regex]=false&columns[40][data]=COD_SIT_TOT_TURNO' \
                    '&columns[40][name]=COD_SIT_TOT_TURNO&columns[40][searchable]=true&columns[40][orderable]=false' \
                    '&columns[40][search][value]=&columns[40][search][regex]=false&columns[41][data]=DESC_SIT_TOT_TURNO' \
                    '&columns[41][name]=DESC_SIT_TOT_TURNO&columns[41][searchable]=true&columns[41][orderable]=false' \
                    '&columns[41][search][value]=&columns[41][search][regex]=false&start=0&search[value]=&search[regex]=false' \
                    '&selected_columns[]=DATA_GERACAO&selected_columns[]=HORA_GERACAO&selected_columns[]=ANO_ELEICAO' \
                    '&selected_columns[]=NUM_TURNO&selected_columns[]=DESCRICAO_ELEICAO&selected_columns[]=SIGLA_UF' \
                    '&selected_columns[]=SIGLA_UE&selected_columns[]=DESCRICAO_UE&selected_columns[]=CODIGO_CARGO' \
                    '&selected_columns[]=DESCRICAO_CARGO&selected_columns[]=NUMERO_PARTIDO&selected_columns[]=SIGLA_PARTIDO' \
                    '&selected_columns[]=NOME_CANDIDATO&selected_columns[]=NUMERO_CANDIDATO&selected_columns[]=CPF_CANDIDATO' \
                    '&selected_columns[]=NOME_URNA_CANDIDATO&selected_columns[]=COD_SITUACAO_CANDIDATURA' \
                    '&selected_columns[]=DES_SITUACAO_CANDIDATURA&selected_columns[]=NOME_PARTIDO&selected_columns[]=CODIGO_LEGENDA' \
                    '&selected_columns[]=SIGLA_LEGENDA&selected_columns[]=COMPOSICAO_LEGENDA&selected_columns[]=NOME_COLIGACAO' \
                    '&selected_columns[]=CODIGO_OCUPACAO&selected_columns[]=DESCRICAO_OCUPACAO&selected_columns[]=DATA_NASCIMENTO' \
                    '&selected_columns[]=NUM_TITULO_ELEITORAL_CANDIDATO&selected_columns[]=IDADE_DATA_ELEICAO' \
                    '&selected_columns[]=CODIGO_SEXO&selected_columns[]=DESCRICAO_SEXO&selected_columns[]=COD_GRAU_INSTRUCAO' \
                    '&selected_columns[]=DESCRICAO_GRAU_INSTRUCAO&selected_columns[]=CODIGO_ESTADO_CIVIL' \
                    '&selected_columns[]=DESCRICAO_ESTADO_CIVIL&selected_columns[]=CODIGO_NACIONALIDADE' \
                    '&selected_columns[]=DESCRICAO_NACIONALIDADE&selected_columns[]=SIGLA_UF_NASCIMENTO' \
                    '&selected_columns[]=CODIGO_MUNICIPIO_NASCIMENTO&selected_columns[]=NOME_MUNICIPIO_NASCIMENTO' \
                    '&selected_columns[]=DESPESA_MAX_CAMPANHA&selected_columns[]=COD_SIT_TOT_TURNO' \
                    '&selected_columns[]=DESC_SIT_TOT_TURNO&cargo=%(cargo)s&agregacao_regional=NaN' \
                    '&agregacao_politica=2&ano=%(ano)s' % {
                    'cargo': cargo,
                    'ano': ano
                }
                filename = u'%s.csv' % hashlib.md5(url.encode('utf-8')).hexdigest()

                # Cria diretório de cache
                if not os.path.exists(os.path.join(settings.BASE_DIR, "cache")):
                    os.makedirs(os.path.join(settings.BASE_DIR, "cache"))

                filepath = os.path.join(settings.BASE_DIR, "cache/" + filename)
                if not os.path.isfile(filepath):
                    content = requests.get(url).content
                    save_cache(content, filepath)

                if cargo in (CARGO.PRESIDENTE,):
                    agreg_regiao = AGR_REGIONAL.BRASIL
                elif cargo in (CARGO.SENADOR, CARGO.DEPUTADO_FEDERAL, CARGO.GOVERNADOR, CARGO.DEPUTADO_ESTADUAL,
                               CARGO.DEPUTADO_DISTRITAL,):
                    agreg_regiao = AGR_REGIONAL.UF
                elif cargo in (CARGO.VEREADOR, CARGO.PREFEITO):
                    agreg_regiao = AGR_REGIONAL.MUNICIPIO

                if Candidatura.objects.filter(ano=ano, cargo=cargo).exists():
                    print('excluindo candidaturas existentes')
                    Candidatura.objects.filter(ano=ano, cargo=cargo).delete()

                count = 0
                count_partido = 0
                count_candidatos = 0
                count_erros = 0
                dataframe = pd.read_csv(filepath, sep=",", dtype=str)
                print('iniciando a conversão (%s)' % filepath)
                for index, data in dataframe.sort_values('NUM_TURNO').iterrows():

                    count += 1

                    if data['DES_SITUACAO_CANDIDATURA'] == 'CANCELADO':
                        continue

                    try:
                        numero = int(data['NUMERO_PARTIDO'])
                    except:
                        print('Linha %d: Candidato sem partido %s' % (count, data['NUMERO_PARTIDO']))
                        count_erros += 1
                        continue

                    partido, novo_partido = Partido.objects.get_or_create(
                        sigla=data['SIGLA_PARTIDO'],
                        numero=numero,
                    )
                    if novo_partido:
                        count_partido += 1

                    legenda = data['CODIGO_LEGENDA']
                    if legenda == '-1':
                        legenda = data['SIGLA_LEGENDA']

                    coligacao, nova_coligacao = Coligacao.objects.get_or_create(
                        ano=ano,
                        cargo=cargo,
                        codigo=legenda,
                    )
                    if nova_coligacao:
                        coligacao.nome = data['NOME_COLIGACAO']
                        coligacao.save()

                    cpf = data['CPF_CANDIDATO']
                    if cpf.find('#') >= 0:
                        dataset = Candidato.objects.filter(nome=data['NOME_CANDIDATO'])
                        if dataset.count() == 0:
                            cpf = gen_id(data['NOME_CANDIDATO'])
                            cpf_ident += 1
                        else:
                            cpf = dataset[0].cpf
                            if dataset.count() > 1:
                                print('Duplicado: %s' % data['NOME_CANDIDATO'])
                    else:
                        cpf = clean_cpf(cpf)

                    try:
                        cand = Candidato.objects.get(cpf=cpf)
                    except Candidato.DoesNotExist:
                        cand = Candidato.objects.get_or_create(
                            nome=data['NOME_CANDIDATO'],
                            cpf=cpf,
                            sexo='M' if int(data['CODIGO_SEXO']) == 2 else 'F',
                            num_acessos=0,
                        )[0]
                        count_candidatos += 1

                    NomePublico.objects.get_or_create(pessoa=cand,nome=data['NOME_URNA_CANDIDATO'])

                    try:
                        numero = int(data['NUMERO_CANDIDATO'])
                    except:
                        numero = 0

                    if data['NUM_TURNO'] == '2':
                        try:
                            candidatura = Candidatura.objects.get(candidato=cand,ano=ano,cargo=cargo)
                            candidatura.resultado = candidatura.resultado + '/' + data['DESC_SIT_TOT_TURNO']
                            candidatura.save()
                        except:
                            print('Linha %d: %s' % (count, cand))
                    else:
                        ue = UE.objects.get(agreg_regiao=agreg_regiao, regiao=str(data['SIGLA_UE']))
                        try:
                            Candidatura(
                                candidato=cand,
                                ano=ano,
                                cargo=cargo,
                                partido=partido,
                                coligacao=coligacao,
                                UE = ue,
                                numero = numero,
                                resultado=data['DESC_SIT_TOT_TURNO'],
                                total_gasto = 0
                            ).save()
                        except:
                            erro = sys.exc_info()
                            print('Linha %d:%s %s %s' % (count, cand.nome, cand.cpf, sys.exc_info()))
                            count_erros += 1

                print('Ano %s / Cargo: %s: %d candidatos importados' % (ano, cargo, count))
                print('Novos candidatos: %d' % count_candidatos)
                print('Novos partidos: %d' % count_partido)
                print('Erros encontrados: %d' % count_erros)