# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from django.db import models

from core.models import Candidatura, Doacao


class Command(BaseCommand):
    help = 'Atualizar Candidatura para agilizar consultas'

    def handle(self, *args, **options):

        print('Atualiza totais das candidaturas')
        count = 0
        for cand in Candidatura.objects.filter(cargo__in=(13,)):
            total = Doacao.objects.filter(candidatura = cand).aggregate(total=models.Sum('valor_at')).get('total')
            cand.total_gasto = total or 0
            cand.primeira = Candidatura.objects.filter(candidato=cand.candidato, ano__lt=cand.ano).exists()
            cand.save()
            count += 1
            if (count % 1000) == 0:
                print(count)
        print('Registros atualizados: %d' % count)