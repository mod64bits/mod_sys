import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from .components import sidebar
app = DjangoDash('Dashbord')   # replaces dash.Dash

template_theme1 = "flatly"
template_theme2 = "vapor"
url_theme1 = dbc.themes.CYBORG
url_theme2 = dbc.themes.COSMO
tab_card = {'height': '100%'}



content = html.Div(id="dashboard-content")
app.layout = dbc.Row([
    dbc.Col([
        dcc.Location(id='url'),
        sidebar.layout
    ], md=2),
    dbc.Col([
        content
        
    ], md=10)
       
    ])



# =========  Callbacks  =========== #

