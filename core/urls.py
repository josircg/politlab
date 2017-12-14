# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from core import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^candidatos/$', views.BuscaCandidatosView.as_view(), name='candidatos_busca'),
    url(r'^candidato/(?P<pk>.+)/$', views.CandidatoView.as_view(), name='candidatos_detalhe'),
    url(r'^candidatura/(?P<pk>.+)/$', views.CandidaturaView.as_view(), name='candidatura_detalhe'),
    url(r'^eleicoes/$', views.BuscaEleicoesView.as_view(), name='eleicoes_busca'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
]