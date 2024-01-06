from django.views.generic import TemplateView

from apps.orcamentos.models import Orcamento


class OrcamentoSimples(TemplateView):
    template_name = 'relatorios/orcamento_simples_template.html'

    def get(self, request, *args, **kwargs):
        self.orcamento = Orcamento.objects.get(id=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orcamento"] = self.orcamento
        return context
