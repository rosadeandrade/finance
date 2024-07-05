import dash
from dash.dependencies import Input, Output
from datetime import date, datetime, timedelta
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from fastapi.datastructures import State
import plotly.express as px
import pandas as pd
import pdb

from app import app

# Generate list of years from 2020 to 2030 for dropdown options
year_options = [{'label': str(year), 'value': year} for year in range(2020, 2031)]
currency_options=['CAD','R$','USD']
expType_options=['Habitacao','Transporte','Alimentacao','Saude','Educacao','Cuidados_Pessoais','Lazer','Taxas','Outros']







# --------------- layout --------------------


layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            html.Legend('Expense Statement', style={'margin-left': '5px'}),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Month',style={'font-weight':'bold'}),
            dcc.Dropdown(
                id='st-month-dropdown',
                options=[
                {'label':datetime.strptime(str(month),'%m').strftime('%B'),'value':f'{month:02}'}
                    for month in range (1,13)
                    ],
                placeholder="...")
                ],width=2,style={'margin-left':'5px'}),
        dbc.Col([
            dbc.Label('Year',style={'font-weight':'bold'}),
            dcc.Dropdown(
                id='st-year-input',
                options=year_options,
                placeholder="..."
                ) 
            ],width=1,style={'margin-left':'5px'}),
        dbc.Col([
            dbc.Label('Currency',style={'font-weight':'bold'}),
            dcc.Dropdown(
                id='st-currency-dropdown',
                options=currency_options,
                value=[],
                placeholder="...")
                ],width=1,style={'margin-left':'5px'}),
        dbc.Col([
            dbc.Label('Exp. Type',style={'font-weight':'bold'}),
            dcc.Dropdown(
                id='st-expType-dropdown',
                options=expType_options,
                value=[],
                placeholder="...")
                ],width=2,style={'margin-left':'5px'}),           
        
        dbc.Col([
            dbc.Label('Total of Expenses',style={'font-weight':'bold'}),
            html.Legend(id='st-expense_amount_card', 
                        style={
                            'font-size': '20px',
                            'background-color':'lightgray',
                            'border-radius':'5px',
                            'border':'1px solid darkgray',
                            'padding-left':'5px',
                            'height':'35px'})
            ],width=3,style={'margin-left':'5px'}),
    ]),
    dbc.Row([
        dbc.Button('Clear', id='btn_clearStatExp', color='danger',style={'width':'100px','text-align':'center','margin-right':'5px'}),
        dbc.Button('Filter', id='btn_filterStatExp', color='success', style={'width':'100px','text-align':'center','margin-right':'5px'})
    ],style={'margin-left':'5px','margin-top':'10px',}),
    dbc.Row([
        html.Legend('Table of Expense', style={'margin-left': '5px','margin-top': '10px'}),
        html.Div(id='table_expense', className='dbc')
    ])
], style={'padding': '10px'})

# ---------------- Callbacks ---------------------


# Add a callback to clear the fields
@app.callback(
    Output('st-month-dropdown', 'value'),
    Output('st-year-input', 'value'),
    Output('st-currency-dropdown', 'value'),
    Output('st-expType-dropdown', 'value'),
    Input('btn_clearStatExp', 'n_clicks')
)
def st_clearFields(n):
    return (
        [],  # default purchase date none
        [],  # default due date none
        [],
        []  # default payment type (empty list or None depending on your initialization)
        
    )

# update the table
@app.callback(
    Output('table_expense', 'children'),
    Output('st-expense_amount_card', 'children'),
    Input('btn_filterStatExp', 'n_clicks'),
    Input('st-month-dropdown', 'value'),
    Input('st-year-input', 'value'),
    Input('st-currency-dropdown', 'value'),
    Input('st-expType-dropdown', 'value'),
    Input('store-expense','data')

)
def filter_expense_data(n_clicks, selected_month, selected_year, selected_currency,selected_expType,data):
    df = pd.DataFrame(data)
    if n_clicks is None or (n_clicks and (not selected_month or not selected_year or not selected_currency)) :
        
        # table
        df = df.sort_values(by=["DueDate","PurchaseDate"])
        columns_to_display = [col for col in df.columns if col !='MonthYearExpenses']
        tableExpense = dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in columns_to_display],
            data=df.to_dict('records'),
            sort_action='native'  # Enable sorting by clicking on the column headers
            )
        
        #sum
        df['TotalPrice'] = pd.to_numeric(df['TotalPrice'], errors='coerce')
        total_by_currency = df.groupby('CurrencyType')['TotalPrice'].sum().reset_index()
        formatted_totals = [f"{row['CurrencyType']} {row['TotalPrice']:,.2f}" for _, row in total_by_currency.iterrows()]
        
        return tableExpense, ' / '.join(formatted_totals)     
  
    
    elif n_clicks:
        # table
        date_filter = f"{selected_year}-{selected_month}-01"
        df_filtered = df[(df['MonthYearExpenses'] == date_filter) & (df['CurrencyType'] == selected_currency) & (df['ExpenseType'] == selected_expType)]
        columns_to_display = [col for col in df.columns if col != 'MonthYearExpenses']
        tableExpense = dash_table.DataTable(
            columns=[{'name': col, 'id': col} for col in columns_to_display],
            data=df_filtered.to_dict('records'),
            sort_action='native'
            )
        #sum
        df_filtered.loc[:,'TotalPrice'] = pd.to_numeric(df_filtered['TotalPrice'], errors='coerce')
        total_by_currency = df_filtered.groupby('CurrencyType')['TotalPrice'].sum().reset_index()
        formatted_totals = [f"{row['CurrencyType']} {row['TotalPrice']:,.2f}" for _, row in total_by_currency.iterrows()]
            
        return tableExpense, ' / '.join(formatted_totals)  

