from django.shortcuts import render

from django.shortcuts import render
from django.views.generic.list import ListView
from .filters import OrdemStatusFilter
from .models import OrdemDeServico
from django.views.generic.edit import CreateView
from  .forms import OrdemServicoForm
from django.views.generic.detail import DetailView


class BaseListFilter(ListView):
    filterset_class = None
    template_name = 'ordens/lista_ordens.html'
    model = OrdemDeServico

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class OrdensLista(BaseListFilter):
    filterset_class = OrdemStatusFilter


class NovaOrdem(CreateView):
    template_name = 'ordens/ordemdeservico_form.html'
    form_class = OrdemServicoForm
    success_url = '/ordens'



class OrdemDeServico(DetailView):
    model = OrdemDeServico

