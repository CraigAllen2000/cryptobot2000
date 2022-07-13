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
import yfinance as yf

#hello
#fig.add_trace(go.Scatter(x=[datetime.datetime(2021,5,1),datetime.datetime(2021,4,1),datetime.datetime(2021,6,1)], y=[140, 150, 145],mode="markers",marker_symbol="x",marker_color="green"))

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(dcc.Graph(id='graph-output1',figure={})),
    html.Div(dcc.Graph(id='graph-output2',figure={},config={
        'displayModeBar': False
    })),
    dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
    )
])



@app.callback(
    Output('graph-output1', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_output_div(n):
    data = yf.download(tickers='BTC-USD', period = '22h', interval = '1m')
    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Scatter(x=data.index,y = data['Close'],mode="markers",marker_color="blue"))

    # Add titles
    fig.update_layout(
        title='Bitcoin live share price evolution',
        yaxis_title='Bitcoin Price (kUS Dollars)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=6, label="6h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    #Show
    fig.show()
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter