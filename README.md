#Laboratório de análise histórica e estatística sobre política partidária

Software que servirá de laboratório para análise do histórico de votações de um determinado candidato e a formulação de variáveis e índices estatísticos que possam auxiliar pesquisadores e jornalistas a entender melhor características que não são aparentes nos dados brutos eleitorais.

A proposta é consolidar vários conjuntos de dados em uma única base consolidada para que se possa no futuro, aplicar técnicas de mineração de dados para a montagem de variáveis não triviais para a obtenção de novos conhecimentos sobre as eleições para os cargos executivos e legislativos. 

A ferramenta faz parte do projeto [FARMi](http://www.farmi.pro.br/sobre) do IBICT/UFRJ e está disponível para acesso online em [PolitLab](http://politlab.farmi.pro.br/)

Também é possível fazer o download da base de dados

##Interface Visual:

A ferramenta inicialmente terá 3 tipos de consultas para o usuário final: Por Político e por Eleição

###1) Por político:

Permitirá a busca pelo nome do político (com direito a desambiguação, mostrando os políticos que tenham mesmo nome, o Estado onde ele concorreu e utilizando o nome utilizado por ele na eleição). 

Após a seleção, o sistema mostra o histórico das votações dele, do mais recente para o mais antigo mostrando as seguintes colunas:

Ano / Cargo / Estado / Cidade / Partido / Coligação / Situação / Posição

Ao clicar em cada uma das votações, a ferramanta abre um quadro que detalhe as seguintes informações:

Dados do Político: Nome / UF Atual / Situação atual

Votos: (número de votos totais) e Situação (Eleito/Não Eleito)

Médias: 
- de Votos que os candidatos eleitos receberam para o mesmo cargo na mesma eleição;
- de Votos Nacionais (%) (média de votos dos eleitos na agregação / total de votos válidos na agregação)

Análise Geográfica:
- Capilaridade: Percentual de Zonas em que recebeu votos (em relação ao total do Estado/Municipio)
- Currularidade: Indicação de que o político detém "currais" eleitorais em determinadas zonas ou municípios. O sistema deverá também fornecer um popup que mostre as zonas eleitorais onde o fenômeno ocorre)

Serão considerados currais eleitorais as seções em que o número de votos do candidato for 30% maior que o total dos votos da referida seção

###2) Por Eleição: Lista os resultados de uma determinada eleição

*Busca inicial*: Ano / Cargo / Estado

Lista um resumo das eleições mostrando a relação entre o número de votos válidos e o número de votos dos candidatos eleitos.  

Também irá mostrar os candidados mais votados com as seguintes colunas: Nome / Partido / Votos / Situação / Posição / Total Investido / Custo do Voto

Para calcular o custo do voto, iremos incorporar a base de Financiamento de Campanha do TSE.

###3) Dashboard

Mostra os registros individuais da base de dados. Nesse ambiente é possível realizar consultas e filtros mais detalhados.  

## Arquitetura

O Politlab foi desenvolvido em Django 1.10 e utiliza base MySQL para consolidar os dados obtidos em 2 fontes primárias:

- CEPESPData - Dados das eleições [1]
- Tribuna - Dados de Financiamento político [2]

A base foi criada para que os usuários pudessem fazer buscas pelo nome público ou pelo nome completo do candidato.

Os dados do CEPESP são utilizados em 2 momentos:
 
- A partir de carga inicial dos candidatos e votos para que as consultas fiquem mais rápidas.
- Durante as consultas do histórico do candidato, busca-se quantos votos foram obtidos. 

[1] http://www.cepesp.io/
[2] https://github.com/rafapolo/tribuna

Detalhes:
- A base de Financiamento de Campanhas deste repositório só contém dados de 2002 em diante.
- Muitas doações para candidatos a vereador e prefeito não foram associadas ao candidato pois não havia a informação de CPF para o candidato.  
