# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, FormView, DetailView, View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login


from django.db.models import F, Q

from core.forms import BuscaEleicoesForm
from core.choices import *
from core.models import Candidato, NomePublico, Candidatura, Votacao

import requests



class HomeView(TemplateView):
    template_name = "core/home.html"


class BuscaCandidatosView(TemplateView):
    template_name = "core/candidatos.html"

    def get_context_data(self, **kwargs):
        context = super(BuscaCandidatosView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            nomespublicos = NomePublico.objects.filter(Q(nome__icontains=q) | Q(pessoa__nome__icontains=q)).select_related(
                'pessoa'
            ).distinct()
            # Atualiza num_acessos
            nomespublicos.update(num_acessos=F('num_acessos')+1)
            context['q'] = q
            context['candidatos'] = Candidato.objects.filter(pessoa_ptr_id__in=nomespublicos.values_list('pessoa', flat=True)).select_related(
                'pessoa_ptr',
            ).prefetch_related(
                'candidatura_set__partido', 'candidatura_set__UE', 'nomepublico_set'
            )
        return context


class CandidatoView(DetailView):
    template_name = "core/candidato.html"
    model = Candidato

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Atualiza num_acessos
        self.object.candidato.num_acessos += 1
        self.object.candidato.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CandidaturaView(DetailView):
    template_name = "core/candidatura.html"
    model = Candidatura


class BuscaEleicoesView(FormView):
    template_name = "core/eleicoes.html"
    form_class = BuscaEleicoesForm

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(BuscaEleicoesView, self).get_context_data(**kwargs)
        context['type'] = self.request.GET.get('type')
        context['ANO_CARGOS'] = ANO_CARGOS_DISPLAY

        if context['type'] == 'geral':
            eleito_choices = ('ELEITO', 'ELEITO POR MÉDIA', 'ELEITO POR MÉDIA', 'ELEITO POR QP', 'ELEITO/ELEITO', '2º TURNO/ELEITO')
            ano = self.request.GET.get('ano')
            cargo = self.request.GET.get('cargo')
            if ano and cargo:
                candidatura_queryset = Candidatura.objects.filter(ano=ano, cargo=cargo)
                candidatura_eleitos_queryset = Candidatura.objects.filter(ano=ano, cargo=cargo, resultado__in=eleito_choices)

                context['candidatos'] = candidatura_queryset.count()
                context['candidatos_eleitos'] = candidatura_eleitos_queryset.count()
                context['partidos'] = len(set(candidatura_queryset.values_list('partido', flat=True)))
                context['partidos_eleitos'] = len(set(candidatura_eleitos_queryset.values_list('partido', flat=True)))
                context['votos_aptos'] = 0
                context['votos_validos'] = 0
                context['perc_validos'] = 0
                context['votos_nominais'] = 0
                context['perc_nominais'] = 0
                context['votos_eleitos'] = 0
                context['perc_eleitos'] = 0

                # Calcula Estatística Global da Eleição
                url = 'http://cepesp.io/api/consulta/tse?cargo=%s&ano=%s&agregacao_regional=0&agregacao_politica=4&format=datatable' % (cargo, ano)

                data_json = requests.get(url).json().get('data')
                if type(data_json) == list:
                    for data in data_json:
                        if data.get('NUM_TURNO') == '1':
                            context['votos_aptos'] += data.get('QTD_APTOS')
                            context['votos_validos'] += data.get('QTD_COMPARECIMENTO')
                            context['votos_nominais'] += data.get('QT_VOTOS_NOMINAIS') + data.get('QT_VOTOS_LEGENDA')

                url = u'http://cepesp.io/api/consulta/tse?ano=%s&cargo=%s&agregacao_regional=0&agregacao_politica=2&columns[0][name]=DESC_SIT_TOT_TURNO&columns[0][search][value]=ELEITO&selected_columns[]=DESC_SIT_TOT_TURNO&selected_columns[]=QTDE_VOTOS&format=datatable' % (ano, cargo)
                data_json = requests.get(url).json().get('data')

                context['votos_eleitos'] = 0
                for data in data_json:
                    if data.get('DESC_SIT_TOT_TURNO') in eleito_choices:
                        context['votos_eleitos'] += data.get('QTDE_VOTOS', 0)

                if context['votos_aptos'] != 0:
                    context['perc_validos'] = round(context['votos_validos'] / context['votos_aptos'] * 100, 2)
                    context['perc_nominais'] = round(context['votos_nominais'] / context['votos_aptos'] * 100, 2)
                    context['perc_eleitos'] = round(context['votos_eleitos'] / context['votos_aptos'] * 100, 2)

                # Candidatos novos
                context['novos'] = candidatura_queryset.filter(primeira=True).count()
                context['novos_eleitos'] = candidatura_eleitos_queryset.filter(primeira=True).count()
        elif context['type'] == 'partidos':
            ano = self.request.GET.get('ano')
            cargo = self.request.GET.get('cargo')
            if ano and cargo:
                context['votacoes'] = Votacao.objects.filter(ano=ano, cargo=cargo, turno="1").order_by('-num_votos')


        elif context['type'] == 'campanhas':
            ano = self.request.GET.get('ano')
            cargo = self.request.GET.get('cargo')
            if ano and cargo:
                context['candidaturas'] = Candidatura.objects.filter(ano=ano, cargo=cargo).order_by('-total_gasto')[:10]
        return context


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        user = authenticate(username='consulta', password='politlab')
        if user is not None:
            login(request, user)
        return HttpResponseRedirect(reverse('admin:index'))