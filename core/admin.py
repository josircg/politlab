# -*- coding: utf-8 -*-
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.db.models import Count

from core.models import (
    Pessoa, Candidato, NomePublico, Partido, Coligacao, Candidatura, Votacao,
    UE, Doador, Doacao, SetorEconomico
)

from core.choices import ANO_CHOICES

class ReadOnlyAdmin(admin.ModelAdmin):
    """Provides a read-only view of a model in Django admin."""
    readonly_fields = []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """ customize add/edit form to remove save / save and continue """
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
           [field.name for field in obj._meta.fields] + \
           [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Pessoa)
class PessoaAdmin(ReadOnlyAdmin):
    list_display = ('nome', 'cpf', 'sexo', )
    search_fields = ('nome', 'cpf', )

@admin.register(Partido)
class PartidoAdmin(ReadOnlyAdmin):
    list_display = ('sigla', 'numero',)
    fields = ('sigla', 'numero',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = get_object_or_404(Partido, pk=object_id)
        extra_context = extra_context or {}
        extra_context['candidaturas'] = []

        for ano, display in ANO_CHOICES:
            extra_context['candidaturas'].append({
                'ano': ano,
                'count': obj.candidatura_set.filter(ano=ano).count()
            })
        return super().change_view(request, object_id, form_url, extra_context)

@admin.register(Coligacao)
class ColigacaoAdmin(ReadOnlyAdmin):
    list_display = ('ano', 'cargo', 'codigo', 'nome', )

class CandidaturaInline(admin.TabularInline):
    model = Candidatura
    extra = 0
    fields = ('ano', 'cargo', 'regiao', 'numero', 'partido', 'resultado' )
    readonly_fields = fields

@admin.register(Candidato)
class CandidatoAdmin(ReadOnlyAdmin):
    list_display = ('nome', 'cpf', 'sexo', )
    fields = ('nome', 'cpf', 'sexo')
    search_fields = ('nome', 'cpf', )
    list_filter = ('sexo', )
    inlines = (CandidaturaInline, )

@admin.register(Candidatura)
class CandidaturaAdmin(ReadOnlyAdmin):
    list_display = ('ano', 'cargo', 'candidato', 'get_ue', 'numero', 'resultado',  )
    list_filter = ('ano', 'cargo', 'partido', )
    search_fields = ('candidato__nome', 'numero' )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('candidato', 'ano', 'cargo', 'agreg_regiao', \
                'regiao', 'numero', 'partido', 'coligacao', 'num_votos', \
                'resultado', 'get_ue', 'primeira', 'total_gasto')
        return ()

@admin.register(NomePublico)
class NomePublicoAdmin(ReadOnlyAdmin):
    list_display = ('pessoa', 'nome', )
    search_fields = ('nome', 'pessoa__nome', 'pessoa__cpf', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('pessoa', 'nome', 'num_acessos', )
        return ('num_acessos', )

@admin.register(Votacao)
class VotacaoAdmin(ReadOnlyAdmin):
    list_display = ('ano', 'cargo', 'turno', 'partido', 'num_votos', 'media')
    search_fields = ('partido__sigla', )
    list_filter = ('ano', 'cargo', )

@admin.register(UE)
class UEAdmin(ReadOnlyAdmin):
    list_display = ('sigla', 'agreg_regiao', 'descricao', 'UF', )
    search_fields = ('sigla', )
    list_filter = ('UF', 'agreg_regiao', )

@admin.register(Doacao)
class DoacoesAdmin(ReadOnlyAdmin):
    list_display = ('candidatura', 'doador', 'dt', 'valor', )
    date_hierarchy = 'dt'

class DoacoesInline(admin.TabularInline):
    model = Doacao
    extra = 0
    fields = ('candidatura', 'valor', 'valor_at', )
    readonly_fields = fields

@admin.register(Doador)
class DoadorAdmin(ReadOnlyAdmin):
    list_display = ('nome', 'cpf', 'cnpj', 'uf', 'setor' )
    list_filter = ('setor',)
    inlines = (DoacoesInline,)

@admin.register(SetorEconomico)
class SetorEconomicoAdmin(ReadOnlyAdmin):
    search_fields = ('descricao',)
    fields = ('descricao',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = get_object_or_404(SetorEconomico, pk=object_id)
        extra_context = extra_context or {}
        extra_context['doadores'] = []

        for ano, display in ANO_CHOICES:

            count = Doacao.objects.filter(dt__year=ano,doador__setor=obj).count()

            extra_context['doadores'].append({
                'ano': ano,
                'count': count
            })
        return super().change_view(request, object_id, form_url, extra_context)

# Custom admin name
admin.site.site_title = u'PolitLab'
admin.site.site_header = u'PolitLab'
admin.site.index_title = u'PolitLab'
