import pandas as pd
import os

# ------------- Expense -------------
# store data
if ('df_expense.csv' in os.listdir()):
    dateColumns = ['PurchaseDate','DueDate','MonthYearExpenses']
    df_expense = pd.read_csv('df_expense.csv', index_col=0, parse_dates=dateColumns, encoding='latin-1')
    
    df_expense["PurchaseDate"]=pd.to_datetime(df_expense['PurchaseDate']).apply(lambda x:x.date())
    df_expense["DueDate"]=pd.to_datetime(df_expense['DueDate']).apply(lambda x:x.date())
    df_expense["MonthYearExpenses"]=pd.to_datetime(df_expense['MonthYearExpenses']).apply(lambda x:x.date())

else:
    data_structure={
        'PurchaseDate':[],
        'DueDate':[],
        'PaymentType':[],
        'CurrencyType':[],
        'Store':[],
        'Item':[],
        'Qty':[],
        'UnitPrice':[],
        'TotalPrice':[],
        'ExpenseType':[],
        'ControlType':[],
        'Note':[],
        'MonthYearExpenses':[]
    }

    df_expense=pd.DataFrame(data_structure)
    df_expense.to_csv('df_expense.csv')
    
# --------------------------------------

# %%
