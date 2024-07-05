import os
import re
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd


from globals import *



# ========= Layout ========= #
layout = dbc.Col([
    html.H1('My Budget', className='text-primary'),
    html.P("By Rosana", className='text-info'),
    html.Hr(),

    # seção perfil
    dbc.Button(
        id='botao_avatar',
        children=[html.Img(src='/assets/selfie.jpg', id='avatar_change', alt='Avatar', className='perfil_avatar')],
        style={'background-color': 'transparent', 'border-color': 'transparent','clip-path': 'circle(50%)'}
    ),

    # seção novo
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='open-new-income', children=['+Income'])
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='open-new-expense', children=['+Expense'])
        ], width=6)
    ]),

    # modal receita

    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição: '),
                    dbc.Input(placeholder='Ex.: dividendos da bolsa, herança,...', id='txt-receita'),
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder='$100.00', id='valor-receita', value=""),
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(
                        id='date-receitas',
                        min_date_allowed=date(2020, 1, 1),
                        max_date_allowed=date(2030, 12, 31),
                        date=datetime.today(),
                        style={"width": "100%"}
                    )
                ], width=4),
                dbc.Col([
                    dbc.Label('Extras'),
                    dbc.Checklist(
                        options=[
                            {'label':'Foi recebida','value':1},
                            {'label':'Receita recorrente','value':2}],
                        value=[1],
                        id='switches-input-receita',
                        switch=True
                    )
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da receita'),
                    dbc.Select(
                        id='select_receita', 
                        options=[], 
                        value=0)
                ], width=4)
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar Categoria", style={'color': 'green'}),
                                dbc.Input(type='text', placeholder='Nova Categoria...', id='input-add-receita',
                                          value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success', id='add-category-receita',
                                           style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(id='category-div-add-receita', style={}),
                            ], width=6),
                            dbc.Col([
                                html.Legend('Excluir categorias', style={'color': 'red'}),
                                dbc.Checklist(
                                    id='checklist-selected-style-receita',
                                    options=[], 
                                    value=[],
                                    label_checked_style={'color': 'red'},
                                    input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'}
                                ),
                                dbc.Button('Remover', color='warning', id='remove-category-receita',
                                           style={'margin-top': '20px'})
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion-receita'),

                html.Div(id='id_teste_receita', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar Receita', id='salvar_receita', color='success'),
                    dbc.Popover(dbc.PopoverBody('Receita Salva'), target='salvar_receita', placement='left',
                                trigger='click')
                ])
            ], style={'margin-top': '25px'})
        ])
    ], style={'background-color': 'rgba(17,140,79,0.5)'},
        id='modal-novo-receita',
        size='lg',
        is_open=False,
        centered=True,
        backdrop=True),
    
    # modal despesa

    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Add Expense')),
        dbc.ModalBody([
             dbc.Row([
                dbc.Col([
                    dbc.Label('Purchase Date '),
                    dcc.DatePickerSingle(
                        id='date_purchaseDate',
                        date=datetime.today(),
                        style={'width':'100%'}
                        ),
                ], width=3),
                dbc.Col([
                    dbc.Label('Due Date '),
                    dcc.DatePickerSingle(
                        id='date_dueDate',
                        date=datetime.today(),
                        style={'width':'100%'}
                    )
                ], width=3),
                dbc.Col([
                    dbc.Label('Payment Type '),
                    dbc.Select(
                        id='select_paymentType',
                        options=['aVista: PicPay','aVista: Bradesco','aVista: R$','Credito: Bradesco','Credito: Itau','Credito: AzulSeguro','Credito: NuBank','Credito: Rico','Credito: PicPay','Credito: C&A','aVista: CAD','aVista: BMO','aVista: Wise','aVista: NuBank','Credito: Triangle'],
                        value=[]
                        ),
                ], width=3,style={'margin-right':'5px'}),
                dbc.Col([
                    dbc.Label('Currency '),
                    dbc.Select(
                        id='select_currencyType',
                        options=['CAD','R$','USD'],
                        value=[]
                        ),
                ], width=2),
            ],style={'margin-bottom': '15px'}),

            dbc.Row([
                dbc.Col([
                    dbc.Label('Store '),
                    dbc.Input(placeholder='Dollarama,Food Basics...', id='txt_store'),
                ], width=12),
            ],style={'margin-bottom': '15px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Item '),
                    dbc.Input(placeholder='Ex.: Shirt, Sneaker,...', id='txt_item'),
                ], width=4),
                dbc.Col([
                    dbc.Label('Qty '),
                    dbc.Input( id='txt_qty', value=""),
                ], width=2),
                dbc.Col([
                    dbc.Label('$ Unit '),
                    dbc.Input( id='txt_unitPrice', value=""),
                ], width=2),
                dbc.Col([
                    dbc.Label('$ Total '),
                    html.Div(id='output_totalPrice'), 
                ], width=2)                
            ],style={'margin-bottom': '15px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Type'),
                    html.Div(id='output_expenseType'), 
                ], width=6),
                dbc.Col([
                    dbc.Label('Control Type:'),
                    dbc.Select(
                        id='select_controlType',
                        options=['Alimentacao(Restaurantes / Bares)','Alimentacao(Supermercado / Padaria)','Cuidados_Pessoais(Salao/Manicure/Estetica)','Cuidados_Pessoais(Vestuario/Calcados/Aces.)','Educacao(Escola/Faculdade/Cursos)','Educacao(Livros / Material Escolar)','Habitacao(Manutencao da Casa)','Habitacao(Aluguel / Financiamento Res.)','Habitacao(Condomínio / Seguro Residencial / Empregada Domestica/IPTU / Internet / TV a Cabo)','Habitacao(Telefone Celular)','Habitacao(Aplicativo)','Lazer(Cinema / Shows / Teatros / Jogos / Partida de Futebol / Clube)','Lazer(Hospedagem)','Outros(Outros)','Outros(Presentes / Pets)','Saude(Consulta Particular / Dentista Particular)','Saude(Academia/Esportes)','Saude(Remedios/ Outros)','Taxas(Tarifa Bancaria / Tarifa Cartao de Credito)','Transporte(Manutencao do Carro / Limpeza Automóvel)','Transporte(Passagens Aereas / Ônibus)','Transporte(Seguro Automóvel / IPVA)','Transporte(Combustível)','Transporte(Taxi / Transporte Privado / Escolar / Estacionamento)','Transporte(Transporte Publico)'],
                        value=[]
                    )
                ], width=6),
                ],style={'margin-bottom': '15px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Note:'),
                    dbc.Input(id='txt_note')
                ]),
                ],style={'margin-bottom': '15px'}),
            dbc.ModalFooter([
                dbc.Button('Add Expense', id='btn_saveExpense', color='success'),
                dbc.Popover(dbc.PopoverBody('Expense Saved'), target='btn_saveExpense', placement='left',
                            trigger='click'),
                dbc.Button('Clear', id='btn_clearExpense', color='danger', className='ml-auto')

            ], style={'margin-top': '25px'}),
        ])
    ], style={'background-color': 'rgba(17,140,79,0.5)'},
        id='modal-new-expense',
        size='lg',
        is_open=False,
        centered=True,
        backdrop=True),

    # seção nav
    html.Hr(),
    dbc.Nav([
        dbc.NavLink('Dashboard', href='/dashboards', active='exact'),
        dbc.NavLink('Extratos', href='/extratos', active='exact')
    ], vertical=True, pills=True, id='nav_buttons', style={'margin-bottom': '25px'}),
], id='sidebar_completed')




# =========  Callbacks  =========== #
# Income
# Expense

# to click and open the button expense
@app.callback(
    Output('modal-new-expense','is_open'),
    Input('open-new-expense','n_clicks'),
    State('modal-new-expense','is_open')
)

def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    
# calculate the total price
@app.callback(
    Output('output_totalPrice', 'children'),
    Input('txt_qty','value'),
    Input('txt_unitPrice', 'value')
)
def calculate_total_price(qty, unitPrice):
    if qty and unitPrice:
            totalPrice = float(qty) * float(unitPrice)
            return f'{totalPrice:.2f}'


# save input data
@app.callback(
    Output('store-expense', 'data'),
    Input('btn_saveExpense', 'n_clicks'),
    [
        State('date_purchaseDate', 'date'),
        State('date_dueDate', 'date'),
        State('select_paymentType', 'value'),
        State('select_currencyType', 'value'),
        State('txt_store', 'value'),
        State('txt_item', 'value'),
        State('txt_qty', 'value'),
        State('txt_unitPrice', 'value'),
        State('output_totalPrice', 'children'),
        State('output_expenseType', 'children'),
        State('select_controlType', 'value'),
        State('txt_note', 'value'),
        State('store-expense','data'),
   
    ]
)
def save_form_expense(n, purchaseDate, dueDate, paymentType, currencyType, store, item, qty, unitPrice, totalPrice, expenseType,controlType, note,dict_expense):
    df_expense = pd.DataFrame(dict_expense)
    if n and not(totalPrice=="" or totalPrice==None):
        purchaseDate = pd.to_datetime(purchaseDate).date()
        dueDate = pd.to_datetime(dueDate).date()
        
         # Format the dueDate to 'YYYY-MM-01'
        month_year_expense = f'{dueDate.year}-{dueDate.month:02}-01'
        
        df_expense.loc[df_expense.shape[0]] = [purchaseDate, dueDate, paymentType, currencyType, store, item, qty, unitPrice, totalPrice, expenseType, controlType,note,month_year_expense]
        df_expense.to_csv('df_expense.csv')
    
    data_return = df_expense.to_dict()
    return data_return

# Add a callback to clear the form fields
@app.callback(
    Output('date_purchaseDate', 'date'),
    Output('date_dueDate', 'date'),
    Output('select_paymentType', 'value'),
    Output('select_currencyType', 'value'),
    Output('txt_store', 'value'),
    Output('txt_item', 'value'),
    Output('txt_qty', 'value'),
    Output('txt_unitPrice', 'value'),
    Output('output_expenseType', 'children', allow_duplicate=True),
    Output('select_controlType', 'value'),
    Output('txt_note', 'value'),
    Input('btn_clearExpense', 'n_clicks'),
     prevent_initial_call=True
)
def clear_expense_form(n):
    return (
        None,  # default purchase date none
        None,  # default due date none
        [],  # default payment type (empty list or None depending on your initialization)
        [],  # default currency type (empty list or None depending on your initialization)
        '',  # default store name
        '',  # default item name
        '',  # default quantity
        '',  # default unit price
        '',  # default expense type 
        [],  # default control type (empty list or None depending on your initialization)
        ''   # default note
    )

# Extracting text before parenthesis and displaying in output_expenseType
@app.callback(
    Output('output_expenseType', 'children', allow_duplicate=True),
    Input('select_controlType', 'value'),
    prevent_initial_call=True,
)
def update_output_expenseType(selected_value):
    if selected_value:
        return selected_value.split('(')[0]
    return ''
