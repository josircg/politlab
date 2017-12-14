# -*- coding: utf-8 -*-
#
# Esta carga é a última a ser feita pois obtem os dados de financiamento de campanha otimizado pelo Projeto Tribuna e
# incorpora os dados das doações à base CEPESP
#
# A base de dados Tribuna está localizado em https://drive.google.com/file/d/1XGzP4gVPXBNE8P8MYHoLvgkUGEWLPO6v/view?usp=sharing
# Após o download deve-se criar um database TSE
#

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from datetime import datetime
from unicodedata import normalize

import sys

from core.models import Candidato, Candidatura, Partido, Doacao, Doador, SetorEconomico
from core.choices import CARGO

class TSE():
    uf = 1
    id = 0
    partido = 2
    cargo = 3
    candidato = 4
    numero = 5
    ano = 6
    cpf_candidato = 7
    doador_original = 8
    doador = 9
    cpf_doador = 10
    cpf_doador_original = 11
    recurso = 12
    setor_economico = 13
    data = 14
    motivo = 15
    fonte = 16
    valor = 17
    valor_at = 18

class Command(BaseCommand):
    help = 'Monta base de Financiamentos'

    def handle(self, *args, **options):

        def normaliza(txt):
            return normalize('NFKD', txt.replace(' ','')).encode('ASCII', 'ignore').decode('ASCII')

        def gen_id(s):
            return abs(hash(normaliza(s))) % (13 ** 10)

        c = connections['tse'].cursor()

        c.execute("select count(*) from doacoes where tipo = 'candidato' and ano = '2012' and valor <> 0")
        row = c.fetchone()
        limit_max = row[0]
        limit = 1
        limit_inc = 10000
        tot_lidos = 0
        tot_doador = 0
        tot_doacoes = 0
        tot_erros = 0
        sem_cpf = 0
        print('Importação de %d registros' % limit_max)

        while limit_inc > 0:

            print('Bloco %d a %d' % (limit, limit+limit_inc))

            c.execute("select * from doacoes where tipo = 'candidato' and ano = '2012' limit %s, %s;", [limit, limit_inc])
#            c.execute("select * from doacoes where tipo = 'candidato' and id = 1490468;")
            rows = c.fetchall()

            limit += limit_inc
            if limit + limit_inc > limit_max:
                limit_inc = limit_max - limit

            if len(rows) == 0:
                break

            for row in rows:

                tot_lidos += 1

                if row[TSE.valor] == 0 or row[TSE.valor] == '':
                    continue

                if row[TSE.cargo] == 'Deputado Estadual':
                    cargo = CARGO.DEPUTADO_ESTADUAL
                elif row[TSE.cargo] == 'Deputado Federal':
                    cargo = CARGO.DEPUTADO_FEDERAL
                elif row[TSE.cargo] == 'Deputado Distrital':
                    cargo = CARGO.DEPUTADO_DISTRITAL
                elif row[TSE.cargo] == 'Senador':
                    cargo = CARGO.SENADOR
                elif row[TSE.cargo] == 'Governador':
                    cargo = CARGO.GOVERNADOR
                elif row[TSE.cargo] == 'Presidente':
                    cargo = CARGO.PRESIDENTE
                elif row[TSE.cargo] == 'Prefeito':
                    cargo = CARGO.PREFEITO
                elif row[TSE.cargo] == 'Vereador':
                    cargo = CARGO.VEREADOR
                else:
                    print('Linha %d: Cargo inválido %s' % (row[TSE.id], row[TSE.cargo]))

                if row[TSE.cpf_candidato]:
                    cpf = row[TSE.cpf_candidato][0:11]
                elif normaliza(row[TSE.candidato]) == normaliza(row[TSE.doador]) and row[TSE.cpf_doador]:
                    cpf = row[TSE.cpf_doador]
                else:
                    cpf = None

                if cargo in (CARGO.GOVERNADOR, CARGO.SENADOR, CARGO.DEPUTADO_FEDERAL, CARGO.DEPUTADO_ESTADUAL):
                    candidatura = Candidatura.objects.filter(ano=row[TSE.ano],
                                                             cargo=cargo,
                                                             numero=row[TSE.numero],
                                                             regiao=row[TSE.uf])
                else:
                    candidatura = None

                if not candidatura or candidatura.count() == 0:
                    if cpf:
                        candidatura = Candidatura.objects.filter(ano=row[TSE.ano], cargo=cargo,
                                                                 candidato__cpf=cpf)
                    else:
                        candidatura = Candidatura.objects.filter(ano=row[TSE.ano], cargo=cargo,
                                                                 candidato__nome=row[TSE.candidato])

                if candidatura.count() == 0:
                    # Verifica se o nome do doador = nome do candidato, se for buscar o candidato pelo CPF
                    if cpf:
                        candidato = Candidato.objects.filter(cpf=cpf)
                    else:
                        candidato = Candidato.objects.filter(nome=row[TSE.candidato])

                    if candidato.count() > 0:
                        print('Linha %d: Candidatura inexistente (%d) %s' % (row[TSE.id], candidato.count(), row[TSE.cargo]))
                    tot_erros += 1
                    continue

                candidatura = candidatura[0]

                if cpf and candidatura.candidato.cpf != cpf:
                    if candidatura.candidato.cpf.find('#') >= 0:
                        candidatura.candidato.cpf = cpf
                        candidatura.candidato.save()

                if row[TSE.cpf_doador] == row[TSE.cpf_candidato] or normaliza(row[TSE.doador]) == normaliza(row[TSE.candidato]) \
                        or row[TSE.motivo] in ('Recursos próprios','Recursos Proprios'):
                    setor = 'Próprio Candidato'
                    cpf_doador = candidatura.candidato.cpf
                else:
                    cpf_doador = row[TSE.cpf_doador].strip()
                    if row[TSE.setor_economico]:
                        setor = row[TSE.setor_economico].strip()
                    else:
                        setor = None

                if setor:
                    setor, novo = SetorEconomico.objects.get_or_create(descricao=setor)

                # Gera Hash pelo ano
                if not cpf_doador:
                    if row[TSE.doador]:
                        cpf_doador = '#%d' % gen_id(row[ TSE.doador])
                    else:
                        cpf_doador = '#%d' % gen_id('INDEFINIDO')
                    sem_cpf += 1

                if len(cpf_doador) > 11:
                    cnpj = cpf_doador
                    cpf = None
                    try:
                        doador = Doador.objects.get(cnpj=cnpj)
                    except Doador.DoesNotExist:
                        doador = None
                else:
                    try:
                        cpf = cpf_doador
                        cnpj = None
                        doador = Doador.objects.get(cpf=cpf)
                    except Doador.DoesNotExist:
                        doador = None

                if doador == None:
                    try:
                        doador = Doador(
                            cpf = cpf,
                            cnpj = cnpj,
                            nome = row[ TSE.doador ],
                            uf = row[ TSE.uf],
                            setor = setor,
                        )
                        doador.save()
                    except:
                        print('Linha %d: Erro ao incluir o doador %s' % (row[TSE.id],sys.exc_info()[0]))
                    tot_doador +=1
                else:
                    if setor and not doador.setor:
                        doador.setor = setor
                        doador.save()

                try:
                    data = datetime.strptime(row[ TSE.data ], "%d/%m/%Y").date()
                except:
                    try:
                        data = datetime.strptime(row[ TSE.data ], "%d-%b-%y").date()
                    except:
                        data = datetime.today()

                try:
                    valor = float(row[ TSE.valor ])
                except:
                    valor = 0

                Doacao(
                    doador = doador,
                    candidatura = candidatura,
                    dt = data,
                    valor = valor,
                    valor_at = row[ TSE.valor_at ]
                ).save()
                tot_doacoes += 1

        c.close()
        print('Total de registros lidos: %d' % tot_lidos)
        print('Novas doações: %d' % tot_doacoes)
        print('Novos doadores: %d' % tot_doador)
        print('Doadores sem CPF: %d' % sem_cpf)
        print('Total de Erros: %d' % tot_erros)