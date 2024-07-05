from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app
import pdb
from dash_bootstrap_templates import ThemeChangerAIO

card_icon={
    'color':'white',
    'textAlign':'center',
    'fontSize':30,
    'margin':'auto'
}
layout = dbc.Col([
    dbc.Row([
            dbc.Col([
                dbc.Label('Month',style={'font-weight':'bold'}),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[
                        {'label':datetime.strptime(str(month),'%m').strftime('%B'),'value':f'{month:02}'}
                        for month in range (1,13)
                        ],
                    placeholder="Select month")
                    ],width=2,style={'margin-left':'5px'}),
            dbc.Col([
                dbc.Label('Year',style={'font-weight':'bold'}),
                dcc.Input(
                    id='year-input',
                    type='number',
                    min=2000,
                    max=2100,
                    placeholder="Enter year"
                    ) 
                ],width=1,style={'margin-left':'5px'})
            ])
    ])
                        
