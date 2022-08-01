from re import T
import plotly.graph_objects as go # or plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import Input, Output
import pandas as pd
import numpy as np
import requests
import json
import datetime
from plotly.subplots import make_subplots
from stock_tools import *
import time
import pytz
import alpaca_trade_api as tradeapi
from random import randint

#fig.add_trace(go.Scatter(x=[datetime.datetime(2021,5,1),datetime.datetime(2021,4,1),datetime.datetime(2021,6,1)], y=[140, 150, 145],mode="markers",marker_symbol="x",marker_color="green"))
global lastprice
global buysX
global buysYyy
global sellsX
global sellsYyy
global port_times
global port
lastprice = 0
buysX = []
buysYyy = [] 
sellsX = []
sellsYyy = []
port_times = []
port = []
api_key = 'PKI3HVXTTVMNE31QVFXI'
api_secret = 'E55gORLlOV9JHZVhOCvshab9G4rQy6ISir7vNFdX'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(
        [dcc.Checklist(
            options=['SMA'],
            id='sma-input'
        ),
        dcc.Checklist(
            options=['EMA'],
            id='ema-input'
        ),
        dcc.Checklist(
            options=['Bollinger Bands'],
            id='bands-input'
        )]
    ),
    html.Div(dcc.Graph(id='graph-output1',figure={})),
    html.Div(dcc.Graph(id='graph-output2',figure={})),
    dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
    )
])



@app.callback(
    Output('graph-output1', 'figure'),
    Output('graph-output2', 'figure'),
    Input(component_id='sma-input', component_property='value'),
    Input(component_id='ema-input', component_property='value'),
    Input(component_id='bands-input', component_property='value'),
    Input('interval-component', 'n_intervals')
)
def update_output_div(sma_input, ema_input, band_input,n):
    global lastprice
    global buysX
    global buysYyy
    global sellsX
    global sellsYyy
    global port_times
    global port

    now = int(time.time())
    from_time = str(now - 86400)
    to_time = str(now)
    date_input_start = '7-27-22 9:30'
    date_input_end = '7-28-22 4:00'
    start_date = datetime.datetime.strptime(date_input_start, '%m-%d-%y %H:%M')
    end_date = datetime.datetime.strptime(date_input_end, '%m-%d-%y %H:%M')
    
    dates = [start_date, end_date]
    tick = 'MRK'
    data, df = getPriceHistory(tick,dates,"minute","day")
    X = convert_time(df["datetime"])
    Y = np.array(df["close"])

    fig1 = go.Figure()
    fig2 = go.Figure()
    sma_data = sma(Y,20)
    ema_data = emma(Y,20)
    lower_band,upper_band = get_Bands(Y,20,2)
    fig1.add_trace(go.Scatter(x=X,y = Y,mode="markers",marker_color="blue"))

    # Add titles
    fig1.update_layout(
        title=tick+" Live Price",
        yaxis_title=tick+' Price (USD)')

    try:
        if sma_input[0] == 'SMA':
            print('sma')
            fig1.add_trace(go.Scatter(x=X, y=sma_data,mode="lines",line_color="#0000ff",name='SMA'))
    except:
        pass
    try:
        if ema_input[0] == 'EMA':
            print('ema')
            fig1.add_trace(go.Scatter(x=X, y=ema_data,mode="lines",line_color="#ff0000",name='EMA')) 
    except:
        pass
    try:
        if band_input[0] == 'Bollinger Bands':
            print('bands')
            fig1.add_trace(go.Scatter(x=X, y=upper_band,mode="lines",line_color="#f0f000",name='Upper Band')) 
            fig1.add_trace(go.Scatter(x=X, y=lower_band,mode="lines",line_color="#f0f000",name='Lower Band')) 
    except:
        pass

    if lastprice != Y[-1]:

        x = randint(0,1)
        if x > 0:
            api.submit_order(symbol=tick, qty=1, side='buy', type='market', time_in_force='day')
            buysX.append(X[-1])
            buysYyy.append(Y[-1])
            print("bought.")
        else:
            api.submit_order(symbol=tick, qty=1, side='sell', type='market', time_in_force='day')
            sellsX.append(X[-1])
            sellsYyy.append(Y[-1])
            print("sold.")
        lastprice = Y[-1]
        a = api.get_account()

        port_times.append(X[-1])
        port.append(a.equity)

    if len(buysX) > 0:
        fig1.add_trace(go.Scatter(x=buysX, y=buysYyy,mode="markers",marker_symbol="x",marker_color="green",name='Bought')) 
    if len(sellsX) > 0:
        fig1.add_trace(go.Scatter(x=sellsX, y=sellsYyy,mode="markers",marker_symbol="x",marker_color="red",name='Sold')) 
    
    #Show
    #fig.show()

    fig2.add_trace(go.Scatter(x=port_times, y=port,mode="lines+markers",marker_color="purple",name='Equity')) 

    return fig1, fig2

if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8000)  # Turn off reloader if inside Jupyter