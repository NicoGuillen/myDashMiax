import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import api_handler

# Objeto dash
# CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Data
ah = api_handler.APIBMEHandler('IBEX')

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


"""
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='MIAX Data Explorer',
    ),

    html.H5(children='mIAx API',
    ),

])
"""
app.layout = html.Div(children=[
    html.H1(
        id='titulo',
        children='MIAX Data Explorer',
    ),

    html.H5(children='mIAx API',
    ),
    html.Label('Index'),
    dcc.Dropdown(
        id='markets',
        options=[
            {'label': 'IBEX', 'value': 'IBEX'},
            {'label': 'DAX', 'value': 'DAX'},
            {'label': 'EUROSTOXX', 'value': 'EUROSTOXX'}
        ],
        value='IBEX'
    ),
    
    html.Label('Ticker'),
    dcc.Dropdown(
            id='tickers',
            # options=dropdown_values, ######### Esto es lo que me esta devolviendo el callback
            # value=dropdown_values[0]['value']
    ),
    
    dcc.Graph(
        id='graph',
    #    figure=fig
    )
])

@app.callback(
    Output(component_id='titulo', component_property='children'),
    Input(component_id='markets', component_property='value')
    )
def change_index(selected_index):
    return 'MIAX Data Explorer:  {}'.format(selected_index) 


@app.callback(
    Output(component_id='tickers', component_property='options'),
    Input(component_id='markets', component_property='value')
    )
def change_index(selected_index):
    ah.market = selected_index
    ticker_master = ah.get_ticker_master()
    tcks = list(ticker_master.ticker)
    dropdown_values = [{'label': tck, 'value': tck} for tck in tcks]
    return dropdown_values
 
"""
# Esto es lo que yo he hehco, pero es ineficiente
@app.callback(
    Output(component_id='tickers', component_property='value'),
    Input(component_id='markets', component_property='value')
    )
def change_index(selected_index):
    ah.market = selected_index
    ticker_master = ah.get_ticker_master()
    tcks = list(ticker_master.ticker)
    dropdown_values = [{'label': tck, 'value': tck} for tck in tcks]
    return dropdown_values[0]['value']
"""

# Esto es para que nos saque el primer valor cuando seleccionemos un mercado
@app.callback(
    Output(component_id='tickers', component_property='value'),
    Input(component_id='tickers', component_property='options') # No vuelvo a llamar a la API, ya tengo los valores en options de tickers
    )
def change_value_ticker(new_options):
    return new_options[0]['value']

"""
# Otra laternativa sería hacerl todo en uno con varios outputs. Tiene que haber tantos return cmoo outputs
@app.callback(
    Output(component_id='tickers', component_property='options'),
    Output(component_id='tickers', component_property='value'),
    Input(component_id='markets', component_property='value')
    )
def change_index(selected_index):
    ah.market = selected_index
    ticker_master = ah.get_ticker_master()
    tcks = list(ticker_master.ticker)
    dropdown_values = [{'label': tck, 'value': tck} for tck in tcks]
    return dropdown_values, dropdown_values[0]['value']
"""
# Falta actualizar el gráfico
# Con este código actualizo en linea
"""
En el ejercicio piden gráfico de velas, esto es línea
@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='tickers', component_property='value') # No vuelvo a llamar a la API, ya tengo los valores en options de tickers
    )
def change_graph(selected_ticker):
    ticker_data = ah.get_close_data_ticker(ticker=selected_ticker)
    fig = px.line(ticker_data)
    return fig
"""
# Para sacar el gráfico de velas


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='tickers', component_property='value') 
)
def change_graph(selected_ticker):
    ticker_data = ah.get_data_ticker(ticker=selected_ticker)
    fig =  go.Figure( 
                go.Candlestick(
                    x=ticker_data.index,
                    open=ticker_data['open'],
                    high=ticker_data['high'],
                    low=ticker_data['low'],
                    close=ticker_data['close']    
                    )
                )
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)

