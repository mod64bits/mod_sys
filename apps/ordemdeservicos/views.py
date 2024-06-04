from django.template.loader import render_to_string
import weasyprint
import tempfile
import datetime
from django.http import HttpResponse
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



class OrdemDeServicoDetalhe(DetailView):
    model = OrdemDeServico

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
