from django.shortcuts import render
from django.template.loader import render_to_string
import weasyprint
import tempfile
import datetime
from django.http import HttpResponse
from django.views import View
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




class PrintOrdem(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'prints/ordem_de_servico.html')


def export_ordem_pdf(request, id):
    ordem = OrdemDeServico.objects.get(id=id)
    html_index = render_to_string('prints/ordem_de_servico.html', {'ordem': ordem})
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(
        stylesheets=[weasyprint.CSS(
            string="""
            <style>
/* 
Import the desired font from Google fonts. 
*/
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

/* 
Define all colors used in this template 
*/
:root{
  --font-color: black;
  --highlight-color: #60D0E4;
  --header-bg-color: #B8E6F1;
  --footer-bg-color: #BFC0C3;
  --table-row-separator-color: #BFC0C3;
}

@page{
  /*
  This CSS highlights how page sizes, margins, and margin boxes are set.
  https://docraptor.com/documentation/article/1067959-size-dimensions-orientation

  Within the page margin boxes content from running elements is used instead of a 
  standard content string. The name which is passed in the element() function can
  be found in the CSS code below in a position property and is defined there by 
  the running() function.
  */
  size:A4;
  margin:8cm 0 3cm 0;

  @top-left{
  	content:element(header);
  }

  @bottom-left{
  	content:element(footer);
  }
}

/* 
The body itself has no margin but a padding top & bottom 1cm and left & right 2cm.
Additionally the default font family, size and color for the document is defined
here.
*/
body{
  margin:0;
  padding:1cm 2cm;
  color:var(--font-color);
  font-family: 'Montserrat', sans-serif;
  font-size:10pt;
}

/*
The links in the document should not be highlighted by an different color and underline
instead we use the color value inherit to get the current texts color.
*/
a{
  color:inherit;
  text-decoration:none;
}

/*
For the dividers in the document we use an HR element with a margin top and bottom 
of 1cm, no height and only a border top of one millimeter.
*/
hr{
  margin:1cm 0;
  height:0;
  border:0;
  border-top:1mm solid var(--highlight-color);
}

/*
The page header in our document uses the HTML HEADER element, we define a height 
of 8cm matching the margin top of the page (see @page rule) and a padding left
and right of 2cm. We did not give the page itself a margin of 2cm to ensure that
the background color goes to the edges of the document.

As mentioned above in the comment for the @page the position property with the 
value running(header) makes this HTML element float into the top left page margin
box. This page margin box repeats on every page in case we would have a multi-page
invoice.
*/
header{
  height:8cm;
  padding:0 2cm;
  position:running(header);
  background-color:var(--header-bg-color);
}

/*
For the different sections in the header we use some flexbox and keep space between
with the justify-content property.
*/
header .headerSection{
  display:flex;
  justify-content:space-between;
}

/*
To move the first sections a little down and have more space between the top of 
the document and the logo/company name we give the section a padding top of 5mm.
*/
header .headerSection:first-child{
  padding-top:.5cm;
}

/*
Similar we keep some space at the bottom of the header with the padding-bottom
property.
*/
header .headerSection:last-child{
  padding-bottom:.5cm;
}

/*
Within the header sections we have defined two DIV elements, and the last one in
each headerSection element should only take 35% of the headers width.
*/
header .headerSection div:last-child{
  width:35%;
}

/*
For the logo, where we use an SVG image and the company text we also use flexbox
to align them correctly.
*/
header .logoAndName{
  display:flex;
  align-items:center;
  justify-content:space-between;
}

/*
The SVG gets set to a fixed size and get 5mm margin right to keep some distance
to the company name.
*/
header .logoAndName svg{
  width:1.5cm;
  height:1.5cm;
  margin-right:.5cm;
}

/*
To ensure the top right section "Invoice #100" starts on the same level as the Logo &
Name we set a padding top of 1cm for this element.
*/
header .headerSection .invoiceDetails{
  padding-top:.5cm;
}

/*
The H3 element "ISSUED TO" gets another 25mm margin to the right to keep some 
space between this header and the client's address.
Additionally this header text gets the hightlight color as font color.
*/
header .headerSection h3{
  margin:0 .75cm 0 0;
  color:var(--highlight-color);
}

/*
Put some margin between the "DUE DATE" and "AMOUNT" headings.
*/
header .headerSection div:last-of-type h3:last-of-type{
  margin-top:.5cm;
}

/*
The paragraphs within the header sections DIV elements get a small 2px margin top
to ensure its in line with the "ISSUED TO" header text.
*/
header .headerSection div p{
  margin-top:2px;
}

/*
All header elements and paragraphs within the HTML HEADER tag get a margin of 0.
*/
header h1,
header h2,
header h3,
header p{
  margin:0;
}

/*
The invoice details should not be uppercase and also be aligned to the right.
*/
header .invoiceDetails,
header .invoiceDetails h2{
  text-align:right;
  font-size:1em;
  text-transform:none;
}

/*
Heading of level 2 and 3 ("DUE DATE", "AMOUNT" and "INVOICE TO") need to be written in 
uppercase, so we use the text-transform property for that.
*/
header h2,
header h3{
  text-transform:uppercase;
}

/*
The divider in the HEADER element gets a slightly different margin than the 
standard dividers.
*/
header hr{
  margin:1cm 0 .5cm 0;
}

/*
Our main content is all within the HTML MAIN element. In this template this are
two tables. The one which lists all items and the table which shows us the 
subtotal, tax and total amount.

Both tables get the full width and collapse the border.
*/
main table{
  width:100%;
  border-collapse:collapse;
}

/*
We put the first tables headers in a THEAD element, this way they repeat on the
next page if our table overflows to multiple pages.

The text color gets set to the highlight color.
*/
main table thead th{
  height:1cm;
  color:var(--highlight-color);
}

/*
For the last three columns we set a fixed width of 2.5cm, so if we would change
the documents size only the first column with the item name and description grows.
*/
main table thead th:nth-of-type(2),
main table thead th:nth-of-type(3),
main table thead th:last-of-type{
  width:2.5cm;
}

/*
The items itself are all with the TBODY element, each cell gets a padding top
and bottom of 2mm.
*/
main table tbody td{
  padding:2mm 0;
}

/*
The cells in the last column (in this template the column containing the total)
get a text align right so the text is at the end of the table.
*/
main table thead th:last-of-type,
main table tbody td:last-of-type{
  text-align:right;
}

/*
By default text within TH elements is aligned in the center, we do not want that
so we overwrite it with an left alignment.
*/
main table th{
  text-align:left;
}

/*
The summary table, so the table containing the subtotal, tax and total amount 
gets a width of 40% + 2cm. The plus 2cm is added because our body has a 2cm padding
but we want our highlight color for the total row to go to the edge of the document.

To move the table to the right side we simply set a margin-left of 60%.
*/
main table.summary{
  width:calc(40% + 2cm);
  margin-left:60%;
  margin-top:.5cm;
}

/*
The row containing the total amount gets its background color set to the highlight 
color and the font weight to bold.
*/
main table.summary tr.total{
  font-weight:bold;
  background-color:var(--highlight-color);
}

/*
The TH elements of the summary table are not on top but the cells on the left side
these get a padding left of 1cm to give the highlight color some space.
*/
main table.summary th{
  padding:4mm 0 4mm 1cm;
}

/*
As only the highlight background color should go to the edge of the document
but the text should still have the 2cm distance, we set the padding right to 
2cm.
*/
main table.summary td{
  padding:4mm 2cm 4mm 0;
  border-bottom:0;
}

/*
The content below the tables is placed in a ASIDE element next to the MAIN element.
To ensure this element is always at the bottom of the page, just above the page 
footer, we use the Prince custom property "-prince-float" with the value bottom.

See Page Floats on https://www.princexml.com/howcome/2021/guides/float/.
*/
aside{
  -prince-float: bottom;
  padding:0 2cm .5cm 2cm;
}

/*
The content itself is shown in 2 columns we use flexbox for this.
*/
aside > div{
  display:flex;
  justify-content:space-between;
}

/*
Each "column" has a width of 45% of the document.
*/
aside > div > div{
  width:45%;
}

/*
The list with the payment options has no bullet points and no margin.
*/
aside > div > div ul{
  list-style-type:none;
  margin:0;
}

/*
The page footer in our document uses the HTML FOOTER element, we define a height 
of 3cm matching the margin bottom of the page (see @page rule) and a padding left
and right of 2cm. We did not give the page itself a margin of 2cm to ensure that
the background color goes to the edges of the document.

As mentioned above in the comment for the @page the position property with the 
value running(footer) makes this HTML element float into the bottom left page margin
box. This page margin box repeats on every page in case we would have a multi-page
invoice.

The content inside the footer is aligned with the help of line-height 3cm and a 
flexbox for the child elements.
*/
footer{
  height:3cm;
  line-height:3cm;
  padding:0 2cm;
  position:running(footer);
  background-color:var(--footer-bg-color);
  font-size:8pt;
  display:flex;
  align-items:baseline;
  justify-content:space-between;
}

/*
The first link in the footer, which points to the company website is highlighted 
in bold.
*/
footer a:first-child{
  font-weight:bold;
}

</style>
<!-- The header element will appear on the top of each page of this invoice document. -->
<header>
  <div class="headerSection">
    <!-- As a logo we take an SVG element and add the name in an standard H1 element behind it. -->
    <div class="logoAndName">
      <svg>
        <circle cx="50%" cy="50%" r="40%" stroke="black" stroke-width="3" fill="black" />
      </svg>
      <h1>Logo &amp; Name</h1>
    </div>
    <!-- Details about the invoice are on the right top side of each page. -->
    <div class="invoiceDetails">
      <h2>Invoice #100</h2>
      <p>
        07 March 2021
      </p>
    </div>
  </div>
  <!-- The two header rows are divided by an blue line, we use the HR element for this. -->
  <hr />
  <div class="headerSection">
    <!-- The clients details come on the left side below the logo and company name. -->
    <div>
      <h3>Invoice to</h3>
      <p>
        <b>Client Name</b>
        <br />
        123 Alphabet Road, Suite 01
        <br />
        Indianapolis, IN 46260
        <br />
        <a href="mailto:clientname@clientwebsite.com">
          clientname@clientwebsite.com
        </a>
        <br />
        317.123.8765
      </p>
    </div>
    <!-- Additional details can be placed below the invoice details. -->
    <div>
      <h3>Due Date</h3>
      <p>
        <b>07 April 2021</b>
      </p>
      <h3>Amount</h3>
      <p>
        <b>$3,500</b>
      </p>
    </div>
  </div>
</header>

<!-- The footer contains the company's website and address. To align the address details we will use flexbox in the CSS style. -->
<footer>
    <a href="https://companywebsite.com">
      companywebsite.com
    </a>
    <a href="mailto:company@website.com">
      company@website.com
    </a>
    <span>
      317.123.8765
    </span>
    <span>
      123 Alphabet Road, Suite 01, Indianapolis, IN 46260
    </span>
</footer>

<!-- In the main section the table for the separate items is added. Also we add another table for the summary, so subtotal, tax and total amount. -->
<main>
  <table>
    <!-- A THEAD element is used to ensure the header of the table is repeated if it consumes more than one page. -->
    <thead>
      <tr>
        <th>Item Description</th>
        <th>Rate</th>
        <th>Amount</th>
        <th>Total</th>
      </tr>
    </thead>
    <!-- The single invoice items are all within the TBODY of the table. -->
    <tbody>
      <tr>
        <td>
          <b>Item Names Goes Here</b>
          <br />
          Description goes here
        </td>
        <td>
          $100
        </td>
        <td>
          4
        </td>
        <td>
          $400.00
        </td>
      </tr>
      <tr>
        <td>
          <b>Lorem Ipsum</b>
          <br />
          Description goes here
        </td>
        <td>
          $250
        </td>
        <td>
          2
        </td>
        <td>
          $500.00
        </td>
      </tr>
      <tr>
        <td>
          <b>Dolor Set Amit Caslum</b>
          <br />
          Description goes here
        </td>
        <td>
          $300
        </td>
        <td>
          1
        </td>
        <td>
          $300.00
        </td>
      </tr>
    </tbody>
  </table>
  <!-- The summary table contains the subtotal, tax and total amount. -->
  <table class="summary">
    <tr>
      <th>
        Subtotal
      </th>
      <td>
        $1200.00
      </td>
    </tr>
    <tr>
      <th>
        Tax 4.7%
      </th>
      <td>
        $000.00
      </td>
    </tr>
    <tr class="total">
      <th>
        Total
      </th>
      <td>
        $12,000.00
      </td>
    </tr>
  </table>
</main>
<!-- Within the aside tag we will put the terms and conditions which shall be shown below the invoice table. -->
<aside>
  <!-- Before the terms and conditions we will add another blue divider line with the help of the HR tag. -->
  <hr />
  <div>
    <div>
      <b>Terms &amp; Conditions</b>
      <p>
        Please make payment within 30 days of issue of the invoice.
      </p>
    </div>
    <div>
      <b>Payment Options</b>
      <ul>
        <li>Paypal</li>
        <li>Credit Card</li>
      </ul>
    </div>
  </div>
</aside>

            """
        )])
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={ordem.cliente}' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response
