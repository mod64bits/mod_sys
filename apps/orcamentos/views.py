from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView
from .models import Orcamento
from .forms import NovoOrcamentoForm


class ListaOrcamentoView(LoginRequiredMixin, ListView):
    model = Orcamento
    template_name = 'orcamentos/lista_orcamentos.html'


class NovoOrcamentoView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'orcamentos/novo_orcamento.html'
    form_class = NovoOrcamentoForm

    success_message = 'Success: Cliente was created.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('orcamentos:orcamento', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        return super(NovoOrcamentoView, self).form_valid(form)


class OrcamentoView(TemplateView):
    template_name = 'orcamentos/orcamento.html'

    # def get(self, request, *args, **kwargs):
    #     orcamento = Orcamento.objects.get(id=kwargs['pk'])
    #
    #     return super(OrcamentoView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orcamento'] = Orcamento.objects.get(id=kwargs['pk'])

        return context
