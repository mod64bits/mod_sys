from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from .import plotly_app
from .. import orcamentos
from ..orcamentos.models import Orcamento


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orcamentos'] = self.dados_orcamentos()
        context['orcamentos_abertos'] = self.orcamentos_abertos()
        return context



    def dados_orcamentos(self):
        nao_enviados = Orcamento.objects.filter(status=0).count()
        em_analise = Orcamento.objects.filter(status=1).count()
        aprovamos = Orcamento.objects.filter(status=2).count()
        cancelados = Orcamento.objects.filter(status=3).count()
        regeitados = Orcamento.objects.filter(status=4).count()

        return {
            "nao_enviados": nao_enviados,
            "em_analise": em_analise,
            "aprovamos": aprovamos,
            "cancelados": cancelados,
            "regeitados": regeitados,
        }

    def orcamentos_abertos(self):
        return Orcamento.objects.filter(status=0)

