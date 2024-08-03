from django.template.loader import render_to_string
import weasyprint
import tempfile
import datetime
from django.http import HttpResponse
from django.views.generic.list import ListView
from .filters import OrdemStatusFilter
from .models import OrdemDeServico, ItemOS
from django.views.generic.edit import CreateView, UpdateView
from  .forms import OrdemServicoForm, MudarStatusForm, EditarOrdemServicoForm, EditarOrdemCompletaForm, AdcionarItemForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalUpdateView, BSModalCreateView
from decimal import Decimal


class BaseListFilter(LoginRequiredMixin, ListView):
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


class NovaOrdem(LoginRequiredMixin, CreateView):
    template_name = 'ordens/ordemdeservico_form.html'
    form_class = OrdemServicoForm
    success_url = '/ordens'


class MudarStatusOrdem(LoginRequiredMixin, BSModalUpdateView):
    model = OrdemDeServico
    form_class = MudarStatusForm
    template_name = 'ordens/mudar_status.html'
    success_url = '/ordens'

class OrdemDeServicoDetalhe(LoginRequiredMixin, DetailView):
    model = OrdemDeServico

class EditarOrdemServicoView(LoginRequiredMixin, BSModalUpdateView):
    model = OrdemDeServico
    form_class = EditarOrdemServicoForm
    template_name = 'ordens/atualizar_ordem.html'
    success_url = '/ordens'

class OrdemDeServicoCompletaView(LoginRequiredMixin, UpdateView):
    model = OrdemDeServico
    form_class = EditarOrdemCompletaForm
    template_name = 'ordens/ordem_completa.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['itens_os'] = ItemOS.objects.filter(ordem_servico_id=self.kwargs['pk'])
        return context

class AdicionarItemOS(BSModalCreateView):
    model = ItemOS
    template_name = 'ordens/adiconar_item_os.html'
    form_class = AdcionarItemForm

    def form_valid(self, form):
        self.ordem = OrdemDeServico.objects.get(id=self.kwargs['pk'])
        form.instance.ordem_servico = self.ordem
        form.instance.total =  Decimal(form.instance.preco * form.instance.quantidade)
        form.instance.ordem_servico = self.ordem
        return super(AdicionarItemOS, self).form_valid(form)


def export_ordem_pdf(request, id):
    ordem = OrdemDeServico.objects.get(id=id)
    html_index = render_to_string('ordens/export-pdf.html', {'ordem': ordem})
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(
        stylesheets=[weasyprint.CSS(string='body { font-family: serif} img {margin: 10px; width: 50px;}')])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={ordem.cliente}' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response
