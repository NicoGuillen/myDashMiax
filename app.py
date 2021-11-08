import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from api_handler import APIBMEHandler

# Objeto dash
# CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Data
ah = APIBMEHandler('IBEX')

# Layout
app.layout = html.Div(children=[
    html.H1(
        children='HOLA QUE TAL',
    ),
    html.H5(
        children='mIAx API',
    ),
    dcc.Dropdown(
        id='markets',
        options=[
            {'label': 'IBEX', 'value': 'IBEX'},
            {'label': 'DAX', 'value': 'DAX'},
            {'label': 'EUROSTOXX', 'value': 'EUROSTOXX'}
        ],
        value='IBEX'
    ),
    dcc.Dropdown(
        id='tickers',
    ),
    dcc.Graph(
        id='graph',
    )
])

# tm = ah.get_ticker_master()
#data_ticker = ah.get_close_data_ticker('SAN')
#print(data_ticker)