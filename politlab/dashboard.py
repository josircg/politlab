# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'
"""

from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for base-tools.
    """
    title = ''
    columns = 2
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        request = context['request']

        self.children += [
            modules.ModelList(
                u'Candidaturas',
                models=('core.models.Pessoa', 'core.models.Candidato', 'core.models.NomePublico',
                        'core.models.Partido', 'core.models.Coligacao', 'core.models.UE', 'core.models.Candidatura',
                        'core.models.Votacao', ),
            ),
            modules.ModelList(
                u'Financiamento de Campanha',
                models=('core.models.SetorEconomico', 'core.models.Doador', 'core.models.Doacao', ),
            ),
            modules.ModelList(
                u'Administração',
                models=('django.contrib.*', ),
            ),
        ]


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for base-tools.
    """

    # we disable title because its redundant with the model list module
    title = ''
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
