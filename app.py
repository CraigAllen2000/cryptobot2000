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
#hello
#fig.add_trace(go.Scatter(x=[datetime.datetime(2021,5,1),datetime.datetime(2021,4,1),datetime.datetime(2021,6,1)], y=[140, 150, 145],mode="markers",marker_symbol="x",marker_color="green"))

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(dcc.Graph(id='graph-output1',figure={})),
    dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
    )
])



@app.callback(
    Output('graph-output1', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_output_div(n):
    from_time = str(1657670093)
    to_time = str(int(time.time()))
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from='+from_time+'&to='+to_time
    x = requests.get(url)
    X = convert_time([row[0] for row in x.json()["prices"]])
    Y = [row[1] for row in x.json()["prices"]]
    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Scatter(x=X,y = Y,mode="markers",marker_color="blue"))

    # Add titles
    fig.update_layout(
        title='Bitcoin Live Price',
        yaxis_title='Bitcoin Price (USD)')

    #Show
    #fig.show()
    return fig

if __name__ == "__main__":
    app.run_server(debug=False, use_reloader=False)  # Turn off reloader if inside Jupyter