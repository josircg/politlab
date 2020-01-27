drop table igrejas;

create table igrejas ( cnpj varchar(14), nome varchar(200) );

create unique index pk_empresa on empresa (cnpj);
create index xfk_socio_empresa on socio (cnpj);

-- não funcionou - fiz pelo pycharm
copy igrejas from './evangelicos/cnpj_igrejas_evangelicas.csv' csv header;
update igrejas set cnpj = lpad(cnpj,14,'0');

select cnpj, count(*) from igrejas
group by cnpj
having count(*) > 1;

-- como foram encontradas duplicadas, vamos removê-las
drop table igrejas_temp;

CREATE TABLE igrejas_temp (LIKE igrejas);

INSERT INTO igrejas_temp(cnpj)
SELECT
    DISTINCT ON (cnpj) cnpj
FROM igrejas;

update igrejas_temp as T
   set nome = (select distinct nome from igrejas where cnpj = t.cnpj)

DROP TABLE igrejas;

ALTER TABLE igrejas_temp RENAME TO igrejas;

create unique index pk_igrejas on igrejas (cnpj);

-- verificar se todas as igrejas estão na base de socios
select * from igrejas as i
 where not exists (select * from empresa as e where e.cnpj = i.cnpj);

-- verificar total de sócios por empresa
-- tem um sujeito que representa mais de 7000 igrejas!
select * FROM
(select cnpj_cpf_do_socio, nome_socio, count(*) from igrejas as i, socio as e
 where i.cnpj = e.cnpj
  group by cnpj_cpf_do_socio, nome_socio
  having count(*) > 2) as maiores
order by 3 desc;

select * from igrejas where cnpj in (
select cnpj from socio where cnpj_cpf_do_socio = '***828616**');

-- existe alguma empresa em que ele não é sócio?
-- não. ele é sócio de todas as empresas
select * from igrejas
where nome = 'IGREJA DO EVANGELHO QUADRANGULAR'
  and cnpj not in (select cnpj from socio where cnpj_cpf_do_socio = '***828616**')

drop table doacao;

create table if not exists doacao
(
	ano_eleicao char(4) not null,
	st_turno char(1) not null,
	sg_uf char(2) not null,
	cd_cargo smallint,
	nr_partido bigint,
	sg_partido varchar(20),
	nr_candidato text,
    nr_cpf_candidato char(11),
	sg_uf_doador char(2),
	nr_cpf_cnpj_doador char(14),
	cd_origem_receita bigint,
	vr_receita numeric(18,2)
);

create index idx_doacao_candidato on doacao (nr_cpf_candidato);
create index idx_doacao_partido on doacao (ano_eleicao,st_turno,sg_uf,sg_partido);
create index idx_doacao_doador on doacao (nr_cpf_cnpj_doador);

drop table doador;

create table doador (
    cpf varchar(11),
    cpf_obf varchar(11),
    nome text
);

create index idx_doador on doador (cpf);
create index idx_doador_obf on doador (cpf_obf);

create table doador_cnpj(
    cpf varchar(11),
    cnpj varchar(14)
);

create table origem_receita
(
    cd_origem_receita bigint,
    ds_origem_receita text
);


create index idx_doador_cnpj on doador_cnpj (cpf, cnpj);

alter table doacao owner to farmi;
alter table doador owner to farmi;
alter table doador_cnpj owner to farmi;

select distinct cd_origem_receita, ds_origem_receita from doacao2018
 where cd_origem_receita is not null

select * from doacao2018
 where length(nr_cpf_cnpj_doador) = 11
   and trim(nm_doador) <> nm_doador_rfb

update doacao2018 set nr_cpf_cnpj_doador = null where nr_cpf_cnpj_doador = '-1';
update doacao2018 set sg_uf_doador = null where sg_uf_doador = '#NULO#';

insert into doacao
  (ano_eleicao, st_turno, sg_uf, cd_cargo, nr_partido, sg_partido, nr_cpf_candidato, sg_uf_doador, cd_origem_receita, nr_cpf_cnpj_doador, vr_receita)
  select
   ano_eleicao, st_turno, sg_uf, cd_cargo, nr_partido, sg_partido, nr_cpf_candidato, sg_uf_doador, cd_origem_receita, nr_cpf_cnpj_doador, vr_doacao
     from doacao2018
   where st_turno is not null;

insert into doador
  (cpf, nome)
  select distinct nr_cpf_cnpj_doador, nm_doador_rfb
    from doacao2018
   where length(nr_cpf_cnpj_doador) = 11

update doador set cpf_obf = concat('***',substr(cpf,4,6),'**');

select * from socio;

select count(*) from doacao2018;
select count(*) from doador;

select sum(vr_receita) from doador d, doacao r
 where d.cpf = r.nr_cpf_cnpj_doador
   and r.nr_cpf_cnpj_doador = r.nr_cpf_candidato;

select sum(vr_receita) from igrejas i, socio s, doador d, doacao r
where i.cnpj = s.cnpj
  and s.cnpj_cpf_do_socio = d.cpf_obf and s.nome_socio = d.nome
  and d.cpf = r.nr_cpf_cnpj_doador;

select sum(vr_receita) from igrejas i, socio s, doador d, doacao r
where i.cnpj = s.cnpj
  and s.cnpj_cpf_do_socio = d.cpf_obf and s.nome_socio = d.nome
  and d.cpf = r.nr_cpf_cnpj_doador
  and r.nr_cpf_cnpj_doador = r.nr_cpf_candidato;