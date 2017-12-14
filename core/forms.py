# -*- coding: utf-8 -*-
from django import forms

from core import choices


class BuscaEleicoesForm(forms.Form):
    ano = forms.ChoiceField(choices=choices.ANO_CHOICES)
    cargo = forms.ChoiceField(choices=choices.CARGO_CHOICES)
    estado = forms.CharField()
    partido = forms.CharField()