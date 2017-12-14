# -*- coding: utf-8 -*-

class AGR_REGIONAL():
    BRASIL = 0
    UF = 2
    MUNICIPIO = 6
    MUNZONA = 7
    ZONA = 8
    MACRO = 1
    MESO = 4
    MICRO = 5

class AGR_POLITICA():
    PARTIDO = 1
    CANDIDATO = 2
    COLIGACAO = 3
    GERAL = 4

class CARGO():
    PRESIDENTE = 1
    GOVERNADOR = 3
    SENADOR = 5
    VEREADOR = 13
    PREFEITO = 11
    DEPUTADO_FEDERAL = 6
    DEPUTADO_ESTADUAL = 7
    DEPUTADO_DISTRITAL = 8

CARGO_CHOICES = (
    (CARGO.VEREADOR, 'Vereador'),
    (CARGO.DEPUTADO_ESTADUAL, 'Deputado Estadual'),
    (CARGO.DEPUTADO_DISTRITAL, 'Deputado Distrital'),
    (CARGO.DEPUTADO_FEDERAL, 'Deputado Federal'),
    (CARGO.SENADOR, 'Senador'),
    (CARGO.PREFEITO, 'Prefeito'),
    (CARGO.GOVERNADOR, 'Governador'),
    (CARGO.PRESIDENTE, 'Presidente'),
)

LOCAL_CHOICES = (
    (AGR_REGIONAL.BRASIL, 'Brasil'),
    (AGR_REGIONAL.UF, 'Estado'),
    (AGR_REGIONAL.MUNICIPIO, 'Municipio'),
)

ANO_CHOICES = (
    (1998, 1998),
    (2000, 2000),
    (2002, 2002),
    (2004, 2004),
    (2006, 2006),
    (2008, 2008),
    (2010, 2010),
    (2012, 2012),
    (2014, 2014),
    (2016, 2016),
)

ELEICAO_FEDERAL = [ CARGO.PRESIDENTE, CARGO.SENADOR, CARGO.GOVERNADOR, CARGO.DEPUTADO_FEDERAL, CARGO.DEPUTADO_ESTADUAL, CARGO.DEPUTADO_DISTRITAL ]
ELEICAO_MUNICIPAL = [ CARGO.VEREADOR, CARGO.PREFEITO ]

ANO_CARGOS =  {
    2012: ELEICAO_MUNICIPAL,
}

'''
ANO_CARGOS =  {
    1998: ELEICAO_FEDERAL,
    2000: ELEICAO_MUNICIPAL,
    2002: ELEICAO_FEDERAL,
    2004: ELEICAO_MUNICIPAL,
    2006: ELEICAO_FEDERAL,
    2008: ELEICAO_MUNICIPAL,
    2010: ELEICAO_FEDERAL,
    2012: ELEICAO_MUNICIPAL,
    2014: ELEICAO_FEDERAL,
    2016: ELEICAO_MUNICIPAL,
}
'''

SEXO = (
    ('M', u'Masculino'),
    ('F', u'Feminino'),
)

ELEICAO_FEDERAL_DISPLAY = (
    (CARGO.PRESIDENTE, 'Presidente'),
    (CARGO.SENADOR, 'Senador'),
    (CARGO.GOVERNADOR, 'Governador'),
    (CARGO.DEPUTADO_FEDERAL, 'Deputado Federal'),
    (CARGO.DEPUTADO_ESTADUAL, 'Deputado Estadual'),
    (CARGO.DEPUTADO_DISTRITAL, 'Deputado Distrital'),
)

ELEICAO_MUNICIPAL_DISPLAY = (
    (CARGO.VEREADOR, 'Vereador'),
    (CARGO.PREFEITO, 'Prefeito'),
)

ANO_CARGOS_DISPLAY = (
    (1998, ELEICAO_FEDERAL_DISPLAY),
    (2000, ELEICAO_MUNICIPAL_DISPLAY),
    (2002, ELEICAO_FEDERAL_DISPLAY),
    (2004, ELEICAO_MUNICIPAL_DISPLAY),
    (2006, ELEICAO_FEDERAL_DISPLAY),
    (2008, ELEICAO_MUNICIPAL_DISPLAY),
    (2010, ELEICAO_FEDERAL_DISPLAY),
    (2012, ELEICAO_MUNICIPAL_DISPLAY),
    (2014, ELEICAO_FEDERAL_DISPLAY),
    (2016, ELEICAO_MUNICIPAL_DISPLAY),
)